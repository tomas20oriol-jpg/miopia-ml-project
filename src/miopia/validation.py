"""Validation scheme shared by the model notebooks.

`evaluate` trains on one set of labels and scores against another, so variants of the training
labels (decision B2 in `docs/assumptions.md`) are measured against the same target. Every model
must be a `Pipeline` that starts with `make_preprocessor`, so nothing is learned from validation rows.
"""

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, balanced_accuracy_score, f1_score, matthews_corrcoef, recall_score,
    roc_auc_score,
)
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline

from miopia.config import RANDOM_STATE
from miopia.features import make_preprocessor

N_SPLITS = 5
N_REPEATS = 10
SUMMARY_METRICS = ["balanced_accuracy", "macro_f1", "accuracy", "mcc"]


def correct_mm_labels(Y: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `Y` where every student with `Combo = MM` has `MM = SI` (decision B2: the training labels
    used from notebook 04 on)."""
    corrected = Y.copy()
    corrected.loc[corrected["Combo"] == "MM", "MM"] = "SI"
    return corrected


def make_strata(Y: pd.DataFrame, target: str) -> pd.Series:
    """Column that defines the folds of `target`; `MM` also keeps the 8 inconsistent students spread out."""
    return Y["Combo"] + "_" + Y["MM"] if target == "MM" else Y[target]


def make_cv(seed: int = RANDOM_STATE) -> RepeatedStratifiedKFold:
    """Repeated stratified K-fold: same strata and seed give the same folds."""
    return RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=seed)


def majority_baseline() -> Pipeline:
    return Pipeline([("prep", make_preprocessor(scale=False)), ("model", DummyClassifier(strategy="most_frequent"))])


def logistic_baseline() -> Pipeline:
    """L2 logistic regression with default strength; class weights match the selection metric (B1)."""
    return Pipeline([("prep", make_preprocessor(scale=True)),
                     ("model", LogisticRegression(class_weight="balanced", max_iter=5000))])


def evaluate(model, X: pd.DataFrame, y_fit: pd.Series, y_score: pd.Series,
             strata: pd.Series, seed: int = RANDOM_STATE) -> tuple[pd.DataFrame, np.ndarray]:
    """Fit on `y_fit`, score against `y_score` on the folds defined by `strata` and `seed`.

    Returns one row of metrics per fold, and the out-of-fold prediction of each student in each
    repeat (shape: students x repeats). SI/NO targets also get AUC and average precision.
    """
    classes = sorted(y_score.unique())
    predictions = np.empty((len(X), N_REPEATS), dtype=object)
    rows = []
    for i, (train, val) in enumerate(make_cv(seed).split(X, strata)):
        repeat, fold = divmod(i, N_SPLITS)
        fitted = clone(model).fit(X.iloc[train], y_fit.iloc[train])
        pred = fitted.predict(X.iloc[val])
        truth = y_score.iloc[val]
        predictions[val, repeat] = pred
        row = {"repeat": repeat, "fold": fold,
               "balanced_accuracy": balanced_accuracy_score(truth, pred),
               "macro_f1": f1_score(truth, pred, labels=classes, average="macro", zero_division=0),
               "accuracy": accuracy_score(truth, pred),
               "mcc": matthews_corrcoef(truth, pred)}
        recalls = recall_score(truth, pred, labels=classes, average=None, zero_division=0)
        row.update({f"recall_{c}": r for c, r in zip(classes, recalls)})
        if classes == ["NO", "SI"]:
            if hasattr(fitted, "predict_proba"):
                score = fitted.predict_proba(X.iloc[val])[:, list(fitted.classes_).index("SI")]
            else:                                    # positive values mean the second class, SI
                score = fitted.decision_function(X.iloc[val])
            row["auc"] = roc_auc_score(truth == "SI", score)
            row["average_precision"] = average_precision_score(truth == "SI", score)
        rows.append(row)
    return pd.DataFrame(rows), predictions


def paired_difference(new: pd.DataFrame, reference: pd.DataFrame, metric: str = "balanced_accuracy") -> dict:
    """Compare two `evaluate` results from the same folds with the bar of B12."""
    diff = new.groupby("repeat")[metric].mean() - reference.groupby("repeat")[metric].mean()
    mean, sd = diff.mean(), diff.std(ddof=1)
    verdict = "clearly better" if mean > sd else "clearly worse" if mean < -sd else "no clear difference"
    return {"mean difference": mean, "sd across repeats": sd, "verdict": verdict}


def selection_test(new: pd.DataFrame, reference: pd.DataFrame) -> dict:
    """Apply the test of B14: `new` passes the reference by route A or route B (B12, B13)."""
    verdicts = {m: paired_difference(new, reference, m) for m in ["balanced_accuracy", "macro_f1", "accuracy"]}
    balanced, f1, accuracy = (verdicts[m]["verdict"] for m in ["balanced_accuracy", "macro_f1", "accuracy"])
    route_a = balanced == "clearly better" and (f1 != "clearly worse" or accuracy == "clearly better")
    route_b = balanced != "clearly worse" and f1 == "clearly better" and accuracy == "clearly better"
    row = {}
    for metric, result in verdicts.items():
        row[f"{metric}: difference"] = result["mean difference"]
        row[f"{metric}: verdict"] = result["verdict"]
    row["passes"] = route_a or route_b
    row["route"] = "A" if route_a else "B" if route_b else ""
    return row
