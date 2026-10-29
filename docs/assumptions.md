# Assumptions and open questions

Everything the brief does not say, or where we chose an interpretation. Claude must not silently decide any of these: use the current status, and if an item is `OPEN` and blocks the work, ask the user. When a decision is made, change its status and say who decided and when. The report must explain every decision that affects results.

Status: `OPEN` (not decided) · `ASSUMED` (working default, please confirm) · `DECIDED` (confirmed by the user/team) · `FACT` (checked in the data or brief).

## About the brief

| # | Assumption | Status | Why it matters / how to settle it |
|---|---|---|---|
| A1 | The `.txt` has one column per target (`M`, `MM`, `Combo`, `DCombo`), tab-separated, a header, one row per test student **in `X_test.csv` order**, no index. | ASSUMED | The brief says only "stored in columns in a .TXT". The test file has no ID column, so row order is the only key. Confirm with the professor if possible. |
| A2 | Labels are written exactly as in `Y_train.csv` (`SI`/`NO`, `C`/`M`/`MM`, `C`/`M1`/`M2`/`MM`), not as the brief's YES/NO. | ASSUMED | The brief says YES/NO but the data says `SI`/`NO`. A grader script would most likely match the data. |
| A3 | `Combo` and `DCombo` are single-label multiclass problems (one label per student), even though the brief says "multi-label". | FACT | Each student has exactly one value in both columns. |
| A4 | `DCombo` has four classes (`C`, `M1`, `M2`, `MM`), not two. | FACT | M1/M2 only split the `M` group; `C` and `MM` pass through unchanged. |
| A5 | "Unique" labels means a single final label set, not de-duplicated rows. | ASSUMED | The brief: even with several models, final labels come from the one we think is best. |
| A6 | The brief's "validation accuracy is not enough" means the report must show more than one metric and the reasoning, not that accuracy is ignored. | ASSUMED | Test accuracy is graded (item 2), so we report it too. |
| A7 | The deadline 23:59 is Spanish local time. | ASSUMED | Upload well before, e.g. by 20:00 on 6 Nov. |

## About the work

| # | Assumption | Status | Why it matters / how to settle it |
|---|---|---|---|
| B1 | **Which metric picks the final model for each target.** Test accuracy is graded, but `MM` has 10 positives in 132 (a model that always says `NO` scores 92%), and the test set has only 24 rows (about 2 `MM` cases expected). | DECIDED | Decided 2026-10-29 (user accepted the proposal): select with balanced accuracy / macro-F1 under repeated stratified CV, report accuracy next to it, and justify the choice in the report. |
| B2 | The 8 students with `Combo = MM` but `MM = NO` (axial length like true myopia magna): train each target on its own column as provided, and evaluate the corrected labels as an extra experiment. | ASSUMED | Notebook 01 now states the three rules; the teammate has not confirmed yet. It changes `MM` labels, `Combo` consistency and what the test is graded against. Rules added after the review of notebook 01: (1) the correction experiment is **scored against the original `MM` labels**, otherwise the two runs measure different targets; (2) the rule for adopting the correction is written down before running it; (3) any consistency check (B3) must never force `MM = SI` just because `Combo = MM`: that pattern is valid in the training labels. Suggestive only (18 rows): the 8 cases cluster by exam date, which points to a labelling criterion that differs by session. |
| B3 | The four targets are modelled separately (a different model per target is allowed). Consistency between them (e.g. `MM = SI` with `M = NO`) is checked after prediction. | ASSUMED | Alternative: predict `DCombo` first and derive the others. Decide in notebook 04 and justify. |
| B4 | The test students come from the same population as the training students. | ASSUMED | Notebook 01 found no strong shift, but with 24 rows the check has little power. |
| B5 | Only classical models are expected (no Keras/PyTorch). | ASSUMED | With 132 rows a neural network is hard to justify. The final slide must say what was used. Ask the user if they want one anyway. |
| B6 | No external data and no pretrained models. | ASSUMED | The brief does not mention either. Ask before using any. |
| B7 | Preprocessing choices from notebook 01 (drop `hº act.cerca sem`, `fecha`, `Grupo fot`; numeric phototype 1-5; one representative per redundant eye column; foreign-ancestors flag; one binary column per relative) stand. | DECIDED | Documented in `CLAUDE.md` and notebook 01. Revisit only with evidence. |
| B8 | The "rules of the Data Science course" (class methods only, no stratified splits, etc.) do **not** apply here. | ASSUMED | This brief explicitly welcomes methods not seen in class. Memory notes from the other course were not applied. |
| B9 | **`phototype` is 45 % missing** once the `E`/`L` entries (a data-entry mix-up with `Grupo fot`) are set to missing: 59 of 132 in train, 9 of 24 in test. Notebook 01 expected about 17 %. | OPEN | Kept in the features for now. Decide inside CV, without looking at the test set: compare with it, without it, and with a missing-indicator, as a model-selection variant in notebook 03/04. Do not pick by looking at its association with the labels outside CV (that leaks). Notebook 02 shows the letters are the `Grupo fot` values (43 of 43), so they carry no phototype information. A reviewer reports that the missing group is less often myopic than the observed group (to verify inside CV, not by peeking). |
| B10 | `fecha` (exam date) is deliberately not used as a feature. | DECIDED | It has no causal link with myopia, and the 8 inconsistent `MM` labels cluster by date, so it could act as a proxy for a labelling artifact. |
| B11 | The retinal columns kept are `OD-Media`, `OS-Media`, `Promedio Nasal` and the SD columns; `CUVAF-Media` and `Promedio Temporal` are dropped because they are exact combinations of those. `Familiar miope num.` is dropped (it is father + mother). | DECIDED | Verified in notebook 02 and in `tests/test_features.py`. |

## About the team and logistics

| # | Assumption | Status | Why it matters / how to settle it |
|---|---|---|---|
| C1 | Who the teammate is and how the work is split. | OPEN | Mandatory final slides. Never invent it: the user fills `[TO FILL]` placeholders. |
| C2 | Who made `01_eda` and with how much AI help. | OPEN | Needed for the AI-usage slide (`docs/ai_usage.md` has `[ask the user]`). |
| C3 | The video is recorded by the user, 10 minutes, after the slides are final. | ASSUMED | Not something Claude can do. |
| C4 | The zip does not include `data/` and may include `models/` only if the notebooks need saved models to run. | ASSUMED | The brief excludes train and test data. Prefer notebooks that retrain in minutes. |
| C5 | The student data are confidential: not committed, not uploaded to any external service, no individual rows in outputs or slides. | ASSUMED | The brief does not say so; this is a conservative default for health data. |

## Change log
- 2026-10-29: B1 decided (balanced accuracy + macro-F1, accuracy reported). B9 stays inside CV. B2 kept with its three rules. Notebook 01 revised (privacy, phototype rate, figures, multiple-test correction).
- 2026-10-29: B2 and B9 extended and B10, B11 added after the reviews of notebooks 01 and 02.
- 2026-10-29: B9 added while writing `features.py` (phototype missingness).
- 2026-10-29: file created from the brief, notebook 01 and the data. Items A3, A4 checked against `Y_train.csv`.
