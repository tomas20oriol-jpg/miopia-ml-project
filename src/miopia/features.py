"""Row-wise cleaning and feature engineering for the myopia data.

`clean_features` is stateless: every output value depends only on its own row, so it can be
applied to train and test alike without leaking information. Everything that is *learned*
from data (imputation values, scaling) lives in `make_preprocessor`, which must be placed
inside an sklearn `Pipeline` so it is fitted within each training fold.

`COLUMN_DECISIONS` is the single source of truth for what happens to each raw column; the
report notebook renders its decision table from it.
"""

import re
import unicodedata

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from miopia.data import load_raw

TARGETS = ["M", "MM", "Combo", "DCombo"]

# raw column -> (action, name(s) of the new feature(s), reason)
COLUMN_DECISIONS: dict[str, tuple[str, str, str]] = {
    "fecha": ("drop", "", "Exam date: no causal link with myopia and contains typos."),
    "edad": ("keep", "age", "Plain numeric."),
    "sexo": ("encode", "female", "Binary flag (Mujer = 1)."),
    "origen antepasados (españa)": ("drop", "", "79 different free-text values for 132 training students: too sparse."),
    "origen antepasados (extranjeros)": (
        "derive", "foreign_ancestors",
        "Free text. 1 if it names any place outside Spain (Andorra counts), 0 if empty, 'No' or only Spain, Navarra or Murcia. "
        "A whitelist: any other Spanish place would count as foreign (none occurs in the data)."),
    "hº deporte sem": ("keep", "sport_h", "Weekly sport hours; kept because it is a component the EDA flagged."),
    "hº naturaleza sem": ("drop", "", "Component of `horas exterior sem` (exact sum)."),
    "hº ocio exteriores sem": ("drop", "", "Component of `horas exterior sem` (exact sum)."),
    "horas exterior sem": ("keep", "outdoor_h", "Total outdoor hours = sport + nature + outdoor leisure."),
    "hº estudiar sem": ("keep", "study_h", "Study hours: near work is a known risk factor."),
    "hº ocio inter sem": ("drop", "", "Component of `horas interior sem` (exact sum with study hours)."),
    "hº act.cerca sem": ("drop", "", "100 % empty."),
    "horas interior sem": (
        "keep", "indoor_h",
        "Total indoor hours = study + indoor leisure. The one missing value is rebuilt from that sum."),
    "Ratio Cerca/Lejos": (
        "drop", "",
        "Equals indoor / outdoor hours whenever outdoor hours > 0 (5 students have 0, where the file holds a value a division cannot give)."),
    "Exterior Mucho": ("encode", "outdoor_much", "SI/NO to 1/0."),
    "Interior Mcho": ("encode", "indoor_much", "SI/NO to 1/0."),
    "fototipo": (
        "derive", "phototype",
        "Number 1-5 from 'Fototipo N'. The values 'E' and 'L' belong to `Grupo fot` (data-entry mix-up) and become missing."),
    "Grupo fot": ("drop", "", "Almost constant (2 'L' values)."),
    "familiar miope": (
        "derive", "father_myopic, mother_myopic, siblings_myopic, relatives_unknown",
        "Lists which relatives are myopic. One flag per relative; 'No lo se' or missing sets `relatives_unknown`."),
    "Familiar miope num.": (
        "drop", "",
        "Counts myopic parents: equals father + mother flags in 150 of 152 known cases. The 4 missing are 'No lo se', already in `relatives_unknown`."),
    "Familiar MM SI/NO": (
        "derive", "family_mm_yes, family_mm_unknown",
        "Myopia magna in the family: yes flag plus an explicit 'does not know' flag."),
    "familiar miope magno": ("drop", "", "Which relative; sparse and covered by `Familiar MM SI/NO`."),
    "pat. Ret. Miop magna": (
        "drop", "",
        "Retinal pathology of myopia magna: a consequence of the target, not a cause. Only 2 positives, both in the MM class."),
    "fumador": ("encode", "smoker", "SI/NO to 1/0."),
    "toma sol": ("encode", "takes_sun", "SI/NO to 1/0."),
    "protege sol": ("encode", "sun_protection", "SI/NO to 1/0."),
    "disp.elec.antes dormir": (
        "encode", "screens_before_sleep", "Ordinal: Nunca = 0, A veces = 1, Siempre = 2."),
    "LA OD": ("drop", "", "Axial length right eye: |r| = 0.99 with the mean. The difference between eyes is given up."),
    "LA OS": ("drop", "", "Axial length left eye: |r| = 0.99 with the mean. The difference between eyes is given up."),
    "LA Media": ("keep", "axial_length", "Mean axial length (mm): the dominant predictor."),
    "Querato OD": ("keep", "kerato_od", "Not an exact combination of other columns."),
    "Querato OD Eje2": ("keep", "kerato_od_axis2", "Not an exact combination of other columns."),
    "Querato OS": ("keep", "kerato_os", "Not an exact combination of other columns."),
    "Querato OS Eje 2": ("keep", "kerato_os_axis2", "Not an exact combination of other columns."),
    "OD-Total": ("drop", "", "Exactly 2 x `OD-Media`."),
    "OD-Media": ("keep", "od_mean", "Representative of the OD-Total / OD-Media pair."),
    "OD-DS": ("keep", "od_sd", "Spread; not a function of the mean."),
    "OS-Total": ("drop", "", "Exactly 2 x `OS-Media`."),
    "OS-Media": ("keep", "os_mean", "Representative of the OS-Total / OS-Media pair."),
    "OS-DS": ("keep", "os_sd", "Spread; not a function of the mean."),
    "CUVAF-Total": ("drop", "", "Exactly `OD-Total` + `OS-Total`."),
    "CUVAF-Media": (
        "drop", "",
        "Equals (OD-Media + OS-Media) / 2 in every training row; one test row does not match its own components."),
    "CUVAF-DS": ("keep", "cuvaf_sd", "Spread; not an exact function of the others."),
    "Promedio Nasal": ("keep", "nasal_mean", "Kept; with the OD and OS means it determines the temporal mean."),
    "DE Nasal": ("keep", "nasal_sd", "Spread."),
    "Suma Nasal": ("drop", "", "Exactly 2 x `Promedio Nasal`."),
    "Promedio Temporal": (
        "drop", "",
        "Nasal + temporal means = OD + OS means exactly, so it is determined by the kept means."),
    "DE Temporal": ("keep", "temporal_sd", "Spread."),
    "Suma Temporal": ("drop", "", "Exactly 2 x `Promedio Temporal`."),
}

FEATURE_COLUMNS = [
    "age", "female", "foreign_ancestors", "sport_h", "outdoor_h", "study_h", "indoor_h",
    "outdoor_much", "indoor_much", "phototype", "father_myopic", "mother_myopic",
    "siblings_myopic", "relatives_unknown", "family_mm_yes",
    "family_mm_unknown", "smoker", "takes_sun", "sun_protection", "screens_before_sleep",
    "axial_length", "kerato_od", "kerato_od_axis2", "kerato_os", "kerato_os_axis2",
    "od_mean", "od_sd", "os_mean", "os_sd", "cuvaf_sd",
    "nasal_mean", "nasal_sd", "temporal_sd",
]

# Words that, alone, do not make an ancestry entry "foreign" (accent-free, lower case).
_SPANISH_WORDS = {"no", "espana", "navarra", "murcia", "y", "de", "del", "la", "el",
                  "norte", "sur", "en", "con"}
_SCREENS = {"nunca": 0, "a veces": 1, "siempre": 2}


def _normalise(text: str) -> str:
    """Lower case and remove accents."""
    text = unicodedata.normalize("NFKD", str(text).lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _is_foreign(text) -> float:
    if pd.isna(text):
        return 0.0
    words = set(re.findall(r"[a-z]+", _normalise(text)))
    return float(bool(words - _SPANISH_WORDS))


def _yes_no(column: pd.Series) -> pd.Series:
    """SI/NO (any case) to 1/0; anything else stays missing."""
    return column.map(lambda v: {"si": 1.0, "no": 0.0}.get(_normalise(v).strip(), np.nan)
                      if pd.notna(v) else np.nan)


def _contains(column: pd.Series, word: str) -> pd.Series:
    return column.map(lambda v: float(word in _normalise(v)) if pd.notna(v) else 0.0)


def clean_features(X: pd.DataFrame) -> pd.DataFrame:
    """Return the model-ready numeric feature table for raw `X` (stateless, row-wise).

    Missing values are *not* imputed here: that is learned from data and belongs in
    `make_preprocessor`. The output has exactly the columns in `FEATURE_COLUMNS`.
    """
    num = lambda col: pd.to_numeric(X[col], errors="coerce").astype(float)  # noqa: E731
    out = pd.DataFrame(index=X.index)

    out["age"] = num("edad")
    out["female"] = X["sexo"].map(
        lambda v: {"mujer": 1.0, "hombre": 0.0}.get(_normalise(v).strip(), np.nan) if pd.notna(v) else np.nan)
    out["foreign_ancestors"] = X["origen antepasados (extranjeros)"].map(_is_foreign)

    out["sport_h"] = num("hº deporte sem")
    out["outdoor_h"] = num("horas exterior sem")
    out["study_h"] = num("hº estudiar sem")
    # Indoor total = study + indoor leisure (exact in all complete rows): rebuild a missing total.
    out["indoor_h"] = num("horas interior sem").fillna(num("hº estudiar sem") + num("hº ocio inter sem"))
    out["outdoor_much"] = _yes_no(X["Exterior Mucho"])
    out["indoor_much"] = _yes_no(X["Interior Mcho"])

    out["phototype"] = pd.to_numeric(
        X["fototipo"].map(lambda v: _normalise(v) if pd.notna(v) else "")
        .str.extract(r"fototipo\s*([1-5])\b")[0], errors="coerce").astype(float)

    relatives = X["familiar miope"]
    out["father_myopic"] = _contains(relatives, "padre")
    out["mother_myopic"] = _contains(relatives, "madre")
    out["siblings_myopic"] = _contains(relatives, "hermanos")
    out["relatives_unknown"] = relatives.map(
        lambda v: 1.0 if pd.isna(v) or "no lo se" in _normalise(v) else 0.0)
    family_mm = X["Familiar MM SI/NO"].map(lambda v: _normalise(v).strip() if pd.notna(v) else "")
    out["family_mm_yes"] = (family_mm == "si").astype(float)
    out["family_mm_unknown"] = (family_mm.isin(["no lo se", ""])).astype(float)

    out["smoker"] = _yes_no(X["fumador"])
    out["takes_sun"] = _yes_no(X["toma sol"])
    out["sun_protection"] = _yes_no(X["protege sol"])
    out["screens_before_sleep"] = X["disp.elec.antes dormir"].map(
        lambda v: _SCREENS.get(_normalise(v).strip(), np.nan) if pd.notna(v) else np.nan).astype(float)

    for new, raw in [("axial_length", "LA Media"), ("kerato_od", "Querato OD"),
                     ("kerato_od_axis2", "Querato OD Eje2"), ("kerato_os", "Querato OS"),
                     ("kerato_os_axis2", "Querato OS Eje 2"), ("od_mean", "OD-Media"),
                     ("od_sd", "OD-DS"), ("os_mean", "OS-Media"), ("os_sd", "OS-DS"),
                     ("cuvaf_sd", "CUVAF-DS"), ("nasal_mean", "Promedio Nasal"),
                     ("nasal_sd", "DE Nasal"), ("temporal_sd", "DE Temporal")]:
        out[new] = num(raw)

    return out[FEATURE_COLUMNS]


def make_preprocessor(scale: bool = True) -> Pipeline:
    """Imputation (median) and optional standardisation, to be fitted inside CV folds.

    Put this as the first step of every model `Pipeline`. Tree-based models do not need
    `scale=True`; linear models, SVMs and k-NN do.
    """
    steps = [("impute", SimpleImputer(strategy="median", keep_empty_features=True))]
    if scale:
        steps.append(("scale", StandardScaler()))
    return Pipeline(steps).set_output(transform="pandas")


def load_clean_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return `X_train`, `Y_train`, `X_test` with the cleaning applied to the features."""
    X_train, Y_train, X_test = load_raw()
    return clean_features(X_train), Y_train, clean_features(X_test)
