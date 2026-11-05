# Myopia ML project (ML course 2026/27)

Predict myopia in 3rd-year medical students (University of Navarra) with four targets:
`M`, `MM` (> 6 dioptres), `Combo` (C / M / MM) and `DCombo` (C / M1 / M2 / MM).

The final labels are in `results/test_labels.txt`. The notebooks are delivered already executed, so they can be read without running anything.

## How to run it

1. Unzip the project and use Python 3.12 or 3.13.
2. Install the dependencies with `poetry install`. The virtualenv is created in `.venv/`; select it as the notebook kernel.
3. On macOS, XGBoost also needs the OpenMP runtime: `brew install libomp`.
4. The CSVs contain student health data and are not included. Copy `X_train.csv`, `Y_train.csv` and `X_test.csv` into `data/raw/`.
5. Run the notebooks in order, from `notebooks/`: `01_eda`, `02_cleaning_features`, `03_baselines_validation`, `04_model_comparison`, `05_final_models`. Notebook 04 runs thousands of cross-validation fits and can take an hour or more; notebook 05 takes a few minutes.

Notebooks 04 and 05 read two sets of saved aggregates from `results/experiments/`, because they take several minutes to compute. To regenerate them:

```bash
poetry run python -m miopia.experiments.nested_protocol
poetry run python -m miopia.experiments.null_calibration
```

**Reproducibility.** Every model uses a fixed seed, so a run gives the same numbers on the same machine with the versions in `poetry.lock`. Install with `poetry install`, not `pip install -e .`, which ignores the lock. With other library versions or another processor, the XGBoost scores can move in the second decimal.

## Layout

| Folder | Content |
|---|---|
| `notebooks/` | The report: numbered notebooks, in English, executed |
| `src/miopia/` | Code used by the notebooks: cleaning, validation and models |
| `src/miopia/experiments/` | The two scripts behind `results/experiments/` |
| `results/` | `test_labels.txt`, and the saved aggregates in `experiments/` |
| `reports/figures/` | Figures for the report and the slides |
| `slides/` | The presentation (`myopia_presentation.pdf`), speaker notes and video scripts |
| `docs/` | `assumptions.md`, every decision and its reason; `ai_usage.md`, the log of generative-AI use |

`src/miopia/models.py` defines the final model of each target in `final_model`.
