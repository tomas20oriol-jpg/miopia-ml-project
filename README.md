# Myopia ML project (ML course 2026/27)

Predict myopia in 3rd-year medical students (University of Navarra) with four targets:
`M`, `MM` (> 6 dioptres), `COMBO` (C / M / MM) and `DCOMBO` (M1 / M2 subtypes).
Brief from the professor: [docs/enunciado_profesor.pdf](docs/enunciado_profesor.pdf).
**Deadline: Friday 6 November, 23:59, via ADI.**

## Setup (WSL / Linux)

```bash
git clone https://github.com/tomas20oriol-jpg/miopia-ml-project.git
cd miopia-ml-project
poetry install
```

The virtualenv is created in `.venv/` (VS Code: *Python: Select Interpreter* → `.venv`).
Run Jupyter with `poetry run jupyter lab` or pick the `.venv` kernel in VS Code.

## Data

The CSVs contain student health data and are **not versioned** (see `.gitignore`).
Copy `X_train.csv`, `Y_train.csv` and `X_test.csv` into `data/raw/`.

## Layout

| Folder | Content |
|---|---|
| `data/raw`, `data/processed` | Original / derived data (ignored by git) |
| `notebooks/` | Numbered report notebooks (`01_eda`, `02_...`), English comments, delivered executed |
| `src/miopia/` | Reusable code (`from miopia.data import load_raw`) |
| `results/` | Final predicted labels (.txt) |
| `reports/figures/` | Figures for the report and slides |
| `slides/` | Presentation (+ AI-usage / work-split slides at the end) |
| `models/` | Saved models (ignored by git) |

## Team workflow

- One branch per task (`git checkout -b eda-juan`), open a PR, merge into `main`.
- `git pull` before starting work; clear notebook outputs conflicts by re-running, not hand-merging.
- Add dependencies with `poetry add <pkg>` and commit `pyproject.toml` + `poetry.lock`.
