---
name: submission-package
description: Produces the final test-labels .txt and the submission zip for the myopia ML project, then runs the final checklist. Use when the final models are chosen and it is time to generate labels, build the zip or prepare the ADI upload.
---

# submission-package

Deadline: Friday 6 November 2026, 23:59 (ADI). Rules come from `docs/enunciado_profesor.pdf`.

## 1. Labels file
- Source: the final notebook (`05_*`), never an ad-hoc script. It must predict `X_test.csv` once, with the model chosen per target, and write `results/test_labels.txt`.
- Format (confirm with the user if unsure): tab-separated, header `M	MM	Combo	DCombo`, one row per test student in the same order as `X_test.csv`, original spelling (`SI`/`NO`, `C`/`M`/`MM`, `M1`/`M2`...). No index column, no NaN.
- Validate with `.venv/bin/python`: row count equals `X_test.csv`, only valid classes per column, and no contradictions between columns (`MM = SI` with `M = NO`).

## 2. Executed notebooks
Run every notebook in order with the `notebook-runner` agent. All cells executed, none in error.

## 3. Zip contents (build in `/tmp` or `~/Desktop`, never inside the repo)
Include: `notebooks/` (executed), `src/`, `results/test_labels.txt`, `reports/figures/`, `slides/`, `pyproject.toml`, `poetry.lock`, `poetry.toml`, `README.md`, `docs/ai_usage.md`, and `models/` only if the notebooks need saved models to run.
Exclude: `data/` (the brief excludes train/test data; also private health data), `.venv/`, `.git/`, `__pycache__/`, `.ipynb_checkpoints/`, `*.csv`.
The video is large: upload it as the brief asks, separately if ADI limits the zip.

```bash
cd ~/miopia-ml-project && zip -r /tmp/miopia_submission.zip notebooks src results/test_labels.txt reports/figures slides pyproject.toml poetry.lock poetry.toml README.md docs/ai_usage.md -x '*/__pycache__/*' '*/.ipynb_checkpoints/*' '*.csv'
unzip -l /tmp/miopia_submission.zip
```

## 4. Final gate
Run the `deliverables-checker` agent. Do not tell the user it is ready until it reports no BLOCKER. Placeholders (`[TO FILL`) in the slides must be filled by the user: never invent the work split.

## 5. Tell the user
Where the zip is, what is still manual (video, ADI upload, filling the team slides) and the days left.
