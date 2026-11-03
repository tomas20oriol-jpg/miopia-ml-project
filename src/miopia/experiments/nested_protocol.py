"""Estimate how optimistic notebook 04 is, by repeating its selection inside outer training folds.

Run with `python -m miopia.experiments.nested_protocol`. It takes several minutes, so notebook 04 reads the
saved aggregates from `results/experiments/nested_protocol.json`. This is an approximation of the protocol:
SVM, tuned logistic regression and the phototype variants are left out, and the random forest and XGBoost use
fixed settings and are candidates only for Combo (they lost on the other targets in notebook 04, a pruning
that used all training students). The test set is not read.
"""

import json

import pandas as pd
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline

from miopia.config import RANDOM_STATE, RESULTS
from miopia.data import load_raw
from miopia.features import make_preprocessor, clean_features, with_axial_corneal_ratio
from miopia.models import BalancedXGBClassifier, ordinal_model, with_tuned_threshold
from miopia.validation import evaluate, logistic_baseline, make_strata, selection_test

SECOND_SEED = RANDOM_STATE + 1
OUTER_SEED = 7
RATIO = "axial_corneal_ratio"
AXIAL = ["axial_length"]


def forest():
    model = RandomForestClassifier(n_estimators=100, min_samples_leaf=3, class_weight="balanced_subsample", random_state=RANDOM_STATE)
    return Pipeline([("prep", make_preprocessor(scale=False)), ("model", model)])


def boosting():
    model = BalancedXGBClassifier(n_estimators=100, max_depth=2, learning_rate=0.1)
    return Pipeline([("prep", make_preprocessor(scale=False)), ("model", model)])


def build_catalog(features):
    return {"axial": (logistic_baseline, AXIAL), "all33": (logistic_baseline, features), "RF": (forest, features),
            "XGB": (boosting, features), "ratio": (logistic_baseline, [RATIO]),
            "axial+ratio": (logistic_baseline, AXIAL + [RATIO]), "all33+ratio": (logistic_baseline, features + [RATIO]),
            "RF+ratio": (forest, features + [RATIO]), "ordinal": (ordinal_model, AXIAL),
            "ordinal+ratio": (ordinal_model, AXIAL + [RATIO])}


FIRST_ROUND = {"M": ["all33"], "MM": ["all33"], "Combo": ["all33", "RF", "XGB"], "DCombo": ["all33"]}
SECOND_ROUND = {"M": ["ratio", "axial+ratio"], "MM": ["ratio", "axial+ratio", "all33+ratio"],
                "Combo": ["ratio", "axial+ratio", "RF+ratio"], "DCombo": ["ratio", "axial+ratio", "ordinal", "ordinal+ratio"]}
FIXED_CHOICE = {"M": ("axial+ratio", None), "MM": ("ratio", "f1_macro"), "Combo": ("RF+ratio", None), "DCombo": ("axial+ratio", None)}


def run_protocol(target, X, Y, catalog):
    """Choose a model and threshold from the training rows only, following notebook 04."""
    strata, y = make_strata(Y, target), Y[target]

    def score(name, seed=RANDOM_STATE):
        factory, columns = catalog[name]
        return evaluate(factory(), X[columns], y, y, strata, seed=seed)[0]

    def advance(current, names, scores):
        for name in names:
            scores.setdefault(name, score(name))
        passing = [n for n in names if selection_test(scores[n], scores[current])["passes"]]
        if passing:
            pick = max(passing, key=lambda n: scores[n]["balanced_accuracy"].mean())
            if selection_test(score(pick, SECOND_SEED), score(current, SECOND_SEED))["passes"]:
                return pick
        return current

    scores = {n: score(n) for n in ["axial", "all33"]}
    reference = max(scores, key=lambda n: scores[n]["balanced_accuracy"].mean())
    current = advance(reference, [n for n in FIRST_ROUND[target] + ["axial"] if n != reference], scores)
    current = advance(current, [n for n in SECOND_ROUND[target] if n != current], scores)

    threshold = None
    if target == "MM":
        factory, columns = catalog[current]
        tuned = {s: evaluate(with_tuned_threshold(factory(), scoring=s), X[columns], y, y, strata)[0]
                 for s in ["balanced_accuracy", "f1_macro"]}
        passing = [s for s, frame in tuned.items() if selection_test(frame, scores[current])["passes"]]
        if passing:
            pick = max(passing, key=lambda s: tuned[s]["balanced_accuracy"].mean())
            second = evaluate(with_tuned_threshold(factory(), scoring=pick), X[columns], y, y, strata, seed=SECOND_SEED)[0]
            threshold = pick if selection_test(second, score(current, SECOND_SEED))["passes"] else None
    return current, threshold


def score_fold(target, repeat, train, val, X, Y, catalog):
    X_train, Y_train = X.iloc[train].reset_index(drop=True), Y.iloc[train].reset_index(drop=True)
    y_val = Y[target].iloc[val]

    def predict(name, threshold):
        factory, columns = catalog[name]
        model = factory() if threshold is None else with_tuned_threshold(factory(), scoring=threshold)
        return model.fit(X_train[columns], Y_train[target]).predict(X[columns].iloc[val])

    def metrics(prefix, predicted):
        return {f"{prefix} balanced accuracy": balanced_accuracy_score(y_val, predicted),
                f"{prefix} macro-F1": f1_score(y_val, predicted, average="macro"),
                f"{prefix} accuracy": accuracy_score(y_val, predicted)}

    chosen, threshold = run_protocol(target, X_train, Y_train, catalog)
    return {"target": target, "repeat": repeat, "chosen": chosen, "threshold": threshold or "none",
            **metrics("whole protocol", predict(chosen, threshold)), **metrics("fixed choice", predict(*FIXED_CHOICE[target])),
            **metrics("axial logistic", predict("axial", None))}


def main():
    X_raw, Y, _ = load_raw()
    clean = clean_features(X_raw)
    X = with_axial_corneal_ratio(clean)
    catalog = build_catalog(list(clean.columns))
    jobs = []
    for target in ["M", "MM", "DCombo", "Combo"]:
        repeats = 3 if target == "Combo" else 4
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=repeats, random_state=OUTER_SEED)
        for i, (train, val) in enumerate(cv.split(X, make_strata(Y, target))):
            jobs.append((target, i // 5, train, val))
    results = pd.DataFrame(Parallel(n_jobs=-1)(delayed(score_fold)(*job, X, Y, catalog) for job in jobs))
    measures = [c for c in results.columns if c not in ("target", "repeat", "chosen", "threshold")]
    output = {"means": results.groupby("target")[measures].mean().round(3).to_dict("index"),
              "sd_across_repeats": results.groupby(["target", "repeat"])["whole protocol balanced accuracy"].mean().groupby("target").std().round(3).to_dict(),
              "chosen_per_fold": {t: g["chosen"].value_counts().to_dict() for t, g in results.groupby("target")},
              "threshold_per_fold_MM": results[results["target"] == "MM"]["threshold"].value_counts().to_dict(),
              "outer_folds": results.groupby("target").size().to_dict()}
    path = RESULTS / "experiments" / "nested_protocol.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=1))
    print(json.dumps(output, indent=1))


if __name__ == "__main__":
    main()
