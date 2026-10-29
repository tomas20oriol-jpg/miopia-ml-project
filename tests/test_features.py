"""Tests for miopia.features. Synthetic rows only: no student data lives in the repo."""

import numpy as np
import pandas as pd
import pytest

from miopia.config import RAW
from miopia.features import (
    COLUMN_DECISIONS, FEATURE_COLUMNS, clean_features, make_preprocessor,
)

HAS_DATA = (RAW / "X_train.csv").exists() and (RAW / "X_test.csv").exists()


def raw_rows(**overrides) -> pd.DataFrame:
    """One-row-per-key raw frame with every raw column present; unset columns are missing."""
    n = max((len(v) for v in overrides.values()), default=1)
    frame = pd.DataFrame({col: [np.nan] * n for col in COLUMN_DECISIONS})
    for col, values in overrides.items():
        frame[col] = values
    return frame


def test_output_columns_and_dtypes():
    out = clean_features(raw_rows(edad=[22, 23]))
    assert list(out.columns) == FEATURE_COLUMNS
    assert all(dtype == float for dtype in out.dtypes)


def test_every_new_feature_is_documented_and_vice_versa():
    named = {name.strip() for _, names, _ in COLUMN_DECISIONS.values()
             for name in names.split(",") if name.strip()}
    assert named == set(FEATURE_COLUMNS)


@pytest.mark.parametrize("text, expected", [
    (np.nan, 0), ("No", 0), ("España", 0), ("Navarra", 0), ("Hungría, España", 1),
    ("Murcia y norte de Italia", 1), ("Cuba, EEUU", 1), ("USA (Boston)", 1), ("Andorra", 1),
    ("italia", 1),
])
def test_foreign_ancestors(text, expected):
    out = clean_features(raw_rows(**{"origen antepasados (extranjeros)": [text]}))
    assert out["foreign_ancestors"].iloc[0] == expected


def test_phototype_keeps_only_real_phototypes():
    out = clean_features(raw_rows(fototipo=["Fototipo 3", "E", "L", np.nan, "Fototipo 1"]))
    assert out["phototype"].iloc[[0, 4]].tolist() == [3, 1]
    assert out["phototype"].iloc[[1, 2, 3]].isna().all()


def test_relatives_flags():
    out = clean_features(raw_rows(**{"familiar miope": [
        "Padre, Madre, Hermanos", "No", "No lo se, Padre, Madre", np.nan, "Hermanos"]}))
    flags = out[["father_myopic", "mother_myopic", "siblings_myopic", "relatives_unknown"]]
    assert flags.values.tolist() == [
        [1, 1, 1, 0], [0, 0, 0, 0], [1, 1, 0, 1], [0, 0, 0, 1], [0, 0, 1, 0]]


def test_family_myopia_magna_flags():
    out = clean_features(raw_rows(**{"Familiar MM SI/NO": ["Si", "No", "No lo se"]}))
    assert out["family_mm_yes"].tolist() == [1, 0, 0]
    assert out["family_mm_unknown"].tolist() == [0, 0, 1]


def test_indoor_total_is_rebuilt_only_when_missing():
    out = clean_features(raw_rows(**{
        "horas interior sem": [np.nan, 50.0], "hº estudiar sem": [10, 20],
        "hº ocio inter sem": [5, 5]}))
    assert out["indoor_h"].tolist() == [15, 50]


def test_binary_and_ordinal_encodings():
    out = clean_features(raw_rows(
        sexo=["Mujer", "Hombre"], fumador=["SI", "no"], **{
            "disp.elec.antes dormir": ["Siempre", "Nunca"], "Exterior Mucho": ["SI", "NO"]}))
    assert out["female"].tolist() == [1, 0]
    assert out["smoker"].tolist() == [1, 0]
    assert out["screens_before_sleep"].tolist() == [2, 0]
    assert out["outdoor_much"].tolist() == [1, 0]


def test_foreign_ancestors_ignores_case_and_accents_but_not_other_countries():
    out = clean_features(raw_rows(**{"origen antepasados (extranjeros)": [
        "ESPAÑA", "navarra", "Murcia", "Andorra", "alemania /filipinas"]}))
    assert out["foreign_ancestors"].tolist() == [0, 0, 0, 1, 1]


def test_sex_is_missing_when_unknown_and_tolerates_spaces():
    out = clean_features(raw_rows(sexo=["Mujer ", "hombre", np.nan, "otro"]))
    assert out["female"].iloc[:2].tolist() == [1, 0]
    assert out["female"].iloc[2:].isna().all()


def test_phototype_parser_is_case_insensitive_and_rejects_out_of_range():
    out = clean_features(raw_rows(fototipo=["fototipo 2", "FOTOTIPO 4", "Fototipo 7", "Fototipo 0"]))
    assert out["phototype"].iloc[:2].tolist() == [2, 4]
    assert out["phototype"].iloc[2:].isna().all()


def test_preprocessor_keeps_all_columns_even_if_one_is_empty_in_training():
    train = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [np.nan] * 3})
    out = make_preprocessor(scale=False).fit(train).transform(train)
    assert list(out.columns) == ["a", "b"]


def test_cleaning_is_row_wise():
    """A row gives the same features alone or inside a batch (no information from other rows)."""
    batch = raw_rows(edad=[21, 22, 23], fototipo=["Fototipo 2", "E", np.nan],
                     **{"horas interior sem": [np.nan, 40.0, 30.0], "hº estudiar sem": [8, 9, 10],
                        "hº ocio inter sem": [4, 4, 4]})
    together = clean_features(batch)
    for i in range(len(batch)):
        alone = clean_features(batch.iloc[[i]])
        pd.testing.assert_frame_equal(alone.reset_index(drop=True),
                                      together.iloc[[i]].reset_index(drop=True))


def test_preprocessor_learns_from_train_only():
    train = pd.DataFrame({"a": [1.0, 2.0, 3.0, np.nan], "b": [10.0, 20.0, 30.0, 40.0]})
    test = pd.DataFrame({"a": [np.nan, 100.0], "b": [np.nan, 5.0]})
    prep = make_preprocessor(scale=False).fit(train)
    out = prep.transform(test)
    assert not out.isna().any().any()
    assert out.iloc[0].tolist() == [2.0, 25.0]  # train medians, not test values


@pytest.fixture(scope="module")
def raw():
    return pd.concat([pd.read_csv(RAW / "X_train.csv"), pd.read_csv(RAW / "X_test.csv")],
                     ignore_index=True)


@pytest.mark.skipif(not HAS_DATA, reason="raw data not present")
class TestAgainstRealData:
    def test_every_raw_column_has_a_decision(self, raw):
        assert set(raw.columns) == set(COLUMN_DECISIONS)

    def test_cleaned_data_has_expected_shape_and_no_infinities(self, raw):
        out = clean_features(raw)
        assert out.shape == (len(raw), len(FEATURE_COLUMNS))
        assert np.isfinite(out.to_numpy(dtype=float)[~out.isna().to_numpy()]).all()

    @pytest.mark.parametrize("big, small", [
        ("OD-Total", "OD-Media"), ("OS-Total", "OS-Media"),
        ("Suma Nasal", "Promedio Nasal"), ("Suma Temporal", "Promedio Temporal")])
    def test_dropped_sums_are_exact_multiples(self, raw, big, small):
        assert np.allclose(raw[big], 2 * raw[small])

    def test_dropped_retinal_columns_are_exact_combinations(self, raw):
        assert np.allclose(raw["OD-Total"] + raw["OS-Total"], raw["CUVAF-Total"])
        assert np.allclose(raw["Suma Nasal"] + raw["Suma Temporal"], raw["CUVAF-Total"])
        # nasal + temporal means = OD + OS means, so the temporal mean is determined by the others
        assert np.allclose(raw["Promedio Nasal"] + raw["Promedio Temporal"],
                           raw["OD-Media"] + raw["OS-Media"])

    def test_dropped_parent_count_matches_the_parent_flags(self, raw):
        known = raw["Familiar miope num."].notna()
        parents = clean_features(raw)[["father_myopic", "mother_myopic"]].sum(axis=1)
        assert (parents[known] == raw.loc[known, "Familiar miope num."]).mean() > 0.98

    def test_dropped_outdoor_components_sum_to_total(self, raw):
        parts = raw[["hº deporte sem", "hº naturaleza sem", "hº ocio exteriores sem"]].sum(axis=1)
        assert np.allclose(raw["horas exterior sem"], parts)

    def test_dropped_indoor_component_and_ratio_are_derived(self, raw):
        total = raw["horas interior sem"].notna()
        assert np.allclose(raw.loc[total, "horas interior sem"],
                           (raw["hº estudiar sem"] + raw["hº ocio inter sem"])[total])
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = raw["horas interior sem"] / raw["horas exterior sem"]
        ok = (raw["horas exterior sem"] > 0) & raw["horas interior sem"].notna()
        assert np.allclose(ratio[ok], raw.loc[ok, "Ratio Cerca/Lejos"])
