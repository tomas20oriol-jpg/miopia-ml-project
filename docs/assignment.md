# Assignment: what the professor asks

Source of truth: `docs/enunciado_profesor.pdf` ("Final Project – ML course 2026/27", 2 pages; identical to `Downloads/README.pdf`). This file restates it as a checklist. If the two ever disagree, the PDF wins. Our interpretation of anything the PDF leaves open lives in [assumptions.md](assumptions.md), never here.

**Deadline: Friday 6 November 2026, 23:59, via ADI.** Group: pairs (one group of 1 or 3 if the class is odd).

## The data
Third-year undergraduate students at the Medical School, University of Navarra. Basic data (age, sex) and metrics known to affect myopia. Files: `X_train.csv`, `Y_train.csv`, `X_test.csv` (test has **no labels**).

## The four predictions

| Name | Brief's wording | In the training data |
|---|---|---|
| `M` | binary: myopia or not, labels YES/NO | `SI` 88 / `NO` 44 |
| `MM` | binary: myopia magna (more than 6 dioptres), YES/NO | `SI` 10 / `NO` 122 |
| `Combo` | "multi-label": M, MM or C (control) | `M` 70, `C` 44, `MM` 18 |
| `DCombo` | "multi-label": myopia split into M1 / M2 | `C` 44, `M1` 39, `M2` 31, `MM` 18 |

Shapes: train 132 x 49 features, test 24 rows.

## Goal and spirit
Produce test labels "as accurate as possible", but "all the process to achieve that goal will count towards the grade". Libraries, functions or architectures not seen in class may be used if we understand them, and this "will actually count positively". The brief's framing: imagine being in a company that gives you this dataset and you must present your work at the end: "will you just show the accuracy on the validation set?"

## Deliverables (one zip, uploaded to ADI)

| # | Deliverable | Rule from the brief | Checked by |
|---|---|---|---|
| 1 | Test labels | The **unique** inferred labels, in columns, in a `.txt`. If several models are presented, the labels must come only from the one we believe is best (may differ per task). | `deliverables-checker` |
| 2 | Report | A Jupyter notebook (or Python scripts) serving as a report. Commented **in English**. Must run with no errors. **Submitted already executed**, output cells visible. | `notebook-runner`, `deliverables-checker` |
| 3 | Code | All files needed to run without errors, except the train and test data. | `deliverables-checker` |
| 4 | Slides | As for a conference or company: briefly the problem, how it was tackled, methodology, results, conclusions. | `slides-writer` |
| 5 | Final slides | (a) work led by each member, or done together; (b) whether the split was 50/50 or different; (c) whether Keras, PyTorch or both were used; (d) how generative AI was used (code, ideas on how to proceed, etc.). | `slides-writer`, `docs/ai_usage.md` |
| 6 | Video | 10 minutes, the recorded presentation. | the user (manual) |

## Evaluation (in this order in the brief)
1. Presentation.
2. Accuracy achieved on the test set.
3. Methodology employed.
4. A well-written report (inside the notebook) that **justifies all actions and functions**.

## Progress (update as work lands)

- [x] `01_eda` executed and merged
- [x] `02` cleaning and feature engineering (executed; methodology and chart reviews done)
- [ ] `03` baselines and validation scheme
- [ ] `04` model comparison per target
- [ ] `05` final models, interpretation, **test labels**
- [ ] Slides, including the mandatory final slides
- [ ] Video
- [ ] Zip built and `deliverables-checker` clean
- [ ] Uploaded to ADI
