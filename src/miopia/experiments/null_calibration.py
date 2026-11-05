"""How often does the selection test of B14 pass when the extra information is useless?

Each run replaces the axial/corneal ratio with a useless version, either with the keratometry shuffled across
students or with random noise, and applies the same test. Run with `python -m miopia.experiments.null_calibration`.
It takes several minutes, so notebook 04 reads the aggregates from `results/experiments/null_calibration.json`.
The test set is not read.
"""

import json

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from miopia.config import RESULTS
from miopia.data import load_raw
from miopia.features import clean_features, with_axial_corneal_ratio
from miopia.validation import correct_mm_labels, evaluate, logistic_baseline, make_strata, selection_test

RUNS = 200
RATIO = "axial_corneal_ratio"
AXIAL = ["axial_length"]
KERATOMETRY = ["kerato_od", "kerato_od_axis2", "kerato_os", "kerato_os_axis2"]


def one_run(target, candidate, reference, kind, run, X, Y):
    rng = np.random.default_rng(run)
    data = X.copy()
    if kind == "shuffled cornea":
        data["useless"] = data["axial_length"] / (337.5 / rng.permutation(data[KERATOMETRY].mean(axis=1).to_numpy()))
    else:
        data["useless"] = rng.normal(size=len(data))
    columns = ["useless" if c == RATIO else c for c in candidate]
    strata = make_strata(Y, target)
    new, _ = evaluate(logistic_baseline(), data[columns], Y[target], Y[target], strata)
    old, _ = evaluate(logistic_baseline(), data[reference], Y[target], Y[target], strata)
    test = selection_test(new, old)
    return {"passes": bool(test["passes"]), "gain": test["balanced_accuracy: difference"]}


def main():
    X_raw, Y_provided, _ = load_raw()
    Y = correct_mm_labels(Y_provided)     # decision B2
    clean = clean_features(X_raw)
    X = with_axial_corneal_ratio(clean)
    features = list(clean.columns)
    comparisons = {"M, axial + ratio vs axial": ("M", AXIAL + [RATIO], AXIAL),
                   "DCombo, axial + ratio vs axial": ("DCombo", AXIAL + [RATIO], AXIAL),
                   "Combo, axial + ratio vs axial": ("Combo", AXIAL + [RATIO], AXIAL),
                   "MM, ratio vs axial": ("MM", [RATIO], AXIAL),
                   "MM, ratio vs all 32": ("MM", [RATIO], features)}
    rows = {}
    for label, (target, candidate, reference) in comparisons.items():
        strata = make_strata(Y, target)
        new, _ = evaluate(logistic_baseline(), X[candidate], Y[target], Y[target], strata)
        old, _ = evaluate(logistic_baseline(), X[reference], Y[target], Y[target], strata)
        real = selection_test(new, old)
        row = {"real gain": round(float(real["balanced_accuracy: difference"]), 3), "real test passes": bool(real["passes"])}
        for kind in ["shuffled cornea", "random noise"]:
            runs = pd.DataFrame(Parallel(n_jobs=-1)(delayed(one_run)(target, candidate, reference, kind, i, X, Y) for i in range(RUNS)))
            row[f"{kind}: pass rate"] = round(float(runs["passes"].mean()), 3)
            row[f"{kind}: 95th percentile of gain"] = round(float(runs["gain"].astype(float).quantile(0.95)), 3)
        rows[label] = row
    output = {"runs_per_row": RUNS, "comparisons": rows}
    path = RESULTS / "experiments" / "null_calibration.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=1))
    print(json.dumps(output, indent=1))


if __name__ == "__main__":
    main()
