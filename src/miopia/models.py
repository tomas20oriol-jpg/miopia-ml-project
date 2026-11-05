"""Candidate models for the comparison in notebook 04, with small grids tuned by nested CV.

With 132 students the grids stay small on purpose: a larger search would mostly fit noise. Every
candidate is a `Pipeline` that starts with `make_preprocessor`, so `GridSearchCV` refits medians and
scaling inside each inner fold.
"""

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold, StratifiedKFold, TunedThresholdClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier

from miopia.config import RANDOM_STATE
from miopia.features import make_preprocessor
from miopia.validation import logistic_baseline

INNER_SPLITS = 3
_INNER_CV = StratifiedKFold(n_splits=INNER_SPLITS, shuffle=True, random_state=RANDOM_STATE)
# One split would make the chosen threshold depend on which few positives land in each fold.
_THRESHOLD_CV = RepeatedStratifiedKFold(n_splits=INNER_SPLITS, n_repeats=10, random_state=RANDOM_STATE)


class BalancedXGBClassifier(ClassifierMixin, BaseEstimator):
    """XGBoost that accepts text labels and weights classes as the other candidates do."""

    def __init__(self, n_estimators=100, max_depth=3, learning_rate=0.1):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate

    def fit(self, X, y):
        encoder = LabelEncoder().fit(y)
        self.classes_ = encoder.classes_
        self.model_ = XGBClassifier(n_estimators=self.n_estimators, max_depth=self.max_depth,
                                    learning_rate=self.learning_rate, subsample=0.8, colsample_bytree=0.5,
                                    n_jobs=1, random_state=RANDOM_STATE)
        self.model_.fit(X, encoder.transform(y), sample_weight=compute_sample_weight("balanced", y))
        return self

    def predict_proba(self, X):
        return self.model_.predict_proba(X)

    def predict(self, X):
        return self.classes_[self.predict_proba(X).argmax(axis=1)]


class OrdinalLogistic(ClassifierMixin, BaseEstimator):
    """Proportional-odds logistic regression with balanced class weights and an L2 penalty.

    One linear score orders the students, and cut-points on it separate the classes in `order`.
    """

    def __init__(self, order=("C", "M1", "M2", "MM"), C=1.0):
        self.order = order
        self.C = C

    def _class_probabilities(self, score, cuts):
        below = expit(cuts[None, :] - score[:, None])
        below = np.hstack([np.zeros((len(score), 1)), below, np.ones((len(score), 1))])
        return np.clip(np.diff(below, axis=1), 1e-12, 1)

    def _unpack(self, params, n_features):
        return params[:n_features], np.cumsum(np.r_[params[n_features], np.exp(params[n_features + 1:])])

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        labels = np.array([self.order.index(v) for v in y])
        weights = compute_sample_weight("balanced", labels)
        n_features = X.shape[1]

        def loss(params):
            beta, cuts = self._unpack(params, n_features)
            probabilities = self._class_probabilities(X @ beta, cuts)
            return -(weights * np.log(probabilities[np.arange(len(labels)), labels])).sum() + beta @ beta / (2 * self.C)

        start = np.r_[np.zeros(n_features), -1.0, np.zeros(len(self.order) - 2)]
        result = minimize(loss, start, method="L-BFGS-B")
        self.coef_, self.cuts_ = self._unpack(result.x, n_features)
        self.classes_ = np.array(self.order)
        return self

    def predict_proba(self, X):
        return self._class_probabilities(np.asarray(X, dtype=float) @ self.coef_, self.cuts_)

    def predict(self, X):
        return self.classes_[self.predict_proba(X).argmax(axis=1)]


def ordinal_model() -> Pipeline:
    """Ordinal logistic regression, standardised inside each training fold."""
    return Pipeline([("prep", make_preprocessor(scale=True)), ("model", OrdinalLogistic())])


CANDIDATES = {
    "Logistic, tuned": (
        True, LogisticRegression(class_weight="balanced", max_iter=5000),
        {"C": [0.01, 0.1, 1, 10]}),
    "SVM (RBF)": (
        True, SVC(class_weight="balanced"),
        {"C": [0.1, 1, 10], "gamma": ["scale", 0.01]}),
    "Random forest": (
        False, RandomForestClassifier(n_estimators=300, class_weight="balanced_subsample", random_state=RANDOM_STATE),
        {"min_samples_leaf": [1, 3, 5], "max_features": ["sqrt", 0.5]}),
    "XGBoost": (
        False, BalancedXGBClassifier(),
        {"n_estimators": [100, 300], "max_depth": [2, 3], "learning_rate": [0.03, 0.1]}),
}


def tuned_model(name: str) -> GridSearchCV:
    """Return candidate `name` as a grid search: the inner loop of the nested CV."""
    scale, estimator, grid = CANDIDATES[name]
    pipeline = Pipeline([("prep", make_preprocessor(scale=scale)), ("model", estimator)])
    return GridSearchCV(pipeline, {f"model__{k}": v for k, v in grid.items()},
                        scoring="balanced_accuracy", cv=_INNER_CV, n_jobs=-1)


def with_tuned_threshold(model, scoring: str = "balanced_accuracy") -> TunedThresholdClassifierCV:
    """Choose the decision threshold of `model` inside the training rows of each outer fold."""
    return TunedThresholdClassifierCV(model, scoring=scoring, cv=_THRESHOLD_CV, random_state=RANDOM_STATE)


def final_model(target: str, features: list[str]):
    """Return the model chosen in notebook 04 for `target`, and the columns it uses."""
    ratio = "axial_corneal_ratio"
    if target in ("M", "DCombo"):
        return logistic_baseline(), ["axial_length", ratio]
    if target == "MM":
        return tuned_model("XGBoost"), features
    return tuned_model("Random forest"), features + [ratio]
