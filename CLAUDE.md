# Myopia ML project (ML course 2026/27)

Final project, done in a pair. Predict myopia in 3rd-year medical students (University of Navarra). Brief: `docs/enunciado_profesor.pdf` (same file as `Downloads/README.pdf`). **Deadline: Friday 6 November 2026, 23:59, via ADI.**

## The assignment

Four targets (`M`, `MM`, `Combo`, `DCombo`) predicted for 24 unlabelled test students; deliverables are labels `.txt`, executed English notebooks, runnable code, slides (with mandatory final slides), a 10-minute video, all zipped. Graded: presentation, test accuracy, methodology, a report that justifies every action. Full detail and checklist: @docs/assignment.md

## Assumptions

Everything the brief leaves open is tracked, with a status, in @docs/assumptions.md. Never silently decide an `OPEN` item that blocks the work: ask the user. When something is decided, update its status and the change log there. Read it at the start of any session.

## Rules for working in this repo

- **Data privacy:** the CSVs are health data of real students. Never commit them (`.gitignore` covers `data/*` and `*.csv`), never paste rows into external tools, and never upload them anywhere (no Notion, Drive, Artifacts, web search). Aggregates and figures are fine.
- **The test set is used once**, for the final prediction. No tuning, feature selection or threshold choice on it. The only fit allowed on `X_test` is none: preprocessing is fitted on train only.
- **Validation:** only 132 training rows and 10 `MM` positives. Use repeated stratified K-fold; put every preprocessing step inside an sklearn `Pipeline` so it is fitted within folds; use nested CV (or a fixed pre-registered criterion) when comparing many models. Report variance across folds, not a single number.
- **Metrics:** never accuracy alone for the imbalanced targets. Report balanced accuracy, macro-F1 and per-class recall (plus MCC or AUC where it fits). Accuracy is still reported, because it is graded.
- **Baselines first** (majority class, logistic regression), then trees/boosting. A more complex model must beat the baseline by a criterion written down beforehand.
- Everything reproducible: `RANDOM_STATE` from `miopia.config`, no hidden state between notebooks.
- Reusable code goes in `src/miopia/` and is imported by notebooks; notebooks stay readable as a report.

## Environment

- Poetry, venv in `.venv/` (`poetry.toml`). Python 3.12. Add packages with `poetry add` (commit `pyproject.toml` + `poetry.lock`), never pip. `pytest` is **not installed yet**: `poetry add --group dev pytest` before writing tests.
- Notebook kernel: `python3` of `.venv`. Run from `notebooks/` with `../.venv/bin/jupyter nbconvert --to notebook --execute --inplace <nb>.ipynb`.
- Paths and seed: `src/miopia/config.py`. Loader: `miopia.data.load_raw()` returns `X_train, Y_train, X_test` untouched.
- Features: `miopia.features` (`clean_features` is row-wise and stateless; `make_preprocessor` learns medians/scaling and must be the first step of every model pipeline; `COLUMN_DECISIONS` documents every raw column). Figures: `miopia.plotting` (`set_style`, `save_fig`, `CLASS_COLORS[task][class]`, `CLASS_MARKERS`). Tests: `.venv/bin/python -m pytest`.
- New notebooks start from `docs/templates/notebook_template.ipynb`.
- Git: one branch per task, PR into `main` (see README). The repo has a teammate: pull before starting, never force-push.

## Language and writing

- Notebook text, code comments, slides: **English**. Talk to the user in the language they write in.
- Each notebook section ends with a short **Findings** cell and each notebook with a **Summary**. Justify decisions in words; few numbers, only those the claim needs; no comparisons with earlier versions of the analysis.
- Do not add anything to a notebook that is not backed by an output in that notebook.

## Charts

Follow [Friends Don't Let Friends](https://github.com/cxli233/FriendsDontLetFriends): bars start at 0, no mean-only bars (show distributions), no pies, ordered heatmaps with viridis. Colour: Okabe-Ito for categories (blue #0072B2, vermilion #D55E00, green #009E73, orange #E69F00, purple #CC79A7, sky #56B4E9; max 6), viridis for continuous, `RdBu_r` only around a meaningful centre, never jet/rainbow/red-green. Check colour-blind and grayscale rendering before delivering. Figures: 300 dpi, white background, saved to `reports/figures/NN_name.png`. They are viewed inline in VS Code notebooks and on slides, so keep labels readable at that size.

## Decisions so far (01 EDA, done)

- Labels are written `SI`/`NO`, not YES/NO as in the brief. Keep the original spelling in the final `.txt`.
- Drop: `hº act.cerca sem` (100% empty), `fecha`, `Grupo fot` (almost constant). Cast all numeric columns to float.
- `fototipo` holds `E`/`L` (values of `Grupo fot`) in 38 rows: keep numeric 1-5, others become missing and are imputed (inside the pipeline).
- Redundant eye columns (OD/OS/mean/total): keep one representative per group. Ancestry free text becomes a "foreign ancestors" flag. `familiar miope` becomes one binary column per relative.
- 8 students have `Combo = MM` but `MM = NO`, with the axial length of true myopia magna. **To be confirmed with the teammate:** train each task on its own column as provided, and test the label correction as an extra experiment.
- Axial length (`LA`) is the dominant predictor. Train and test look like the same population, but with 24 test rows the check has little power.

## Decisions so far (02, done)

- 49 raw columns become 33 numeric features (20 dropped: 1 empty, 12 exact or almost exact combinations, 7 judgement calls, all justified in `COLUMN_DECISIONS` and notebook 02). The standardised matrix has full rank.
- `phototype` is 45 % missing (the letters in `fototipo` are `Grupo fot` values): kept for now, decision B9 happens inside CV.
- `fecha` and `pat. Ret. Miop magna` are not used (B10, and a consequence of the target).

## Plan

`01` EDA (done) → `02` cleaning + feature engineering (done) → `03` baselines + validation scheme → `04` model comparison per target (incl. at least one model not seen in class, explained) → `05` final models, interpretation (permutation importance / SHAP), error analysis, **test labels** → slides, video, zip.

## Agents (`.claude/agents/`)

Delegate instead of doing the work inline. All use Opus except the runner (mechanical).

| When | Agent | Model | Access |
|---|---|---|---|
| After editing a notebook | `notebook-runner`: executes it, returns errors, key outputs, new figures | haiku | runs only |
| Before trusting any CV number or choosing a model | `methodology-reviewer`: leakage, validation, metrics, claims vs outputs | opus | read-only |
| Heavy model comparisons (many CV fits) | `model-experimenter`: runs the grid in `src/` scripts, returns a compact table | opus | writes `src/miopia/` and `results/experiments/` only |
| After creating a chart | `chart-reviewer`: Friends Don't Let Friends, colour accessibility, readability | opus | read-only |
| For slides | `slides-writer`: builds the deck from real outputs; leaves team facts as placeholders | opus | writes `slides/` and `docs/` only |
| Before zipping | `deliverables-checker`: audits every rule of the brief | opus | read-only |

Loop per phase: build the notebook with the user → `notebook-runner` → `methodology-reviewer` + `chart-reviewer` in parallel → fix → next phase. Before submission: `deliverables-checker` until it returns no blockers.

## Skills

- Project (`.claude/skills/`): `submission-package` (labels `.txt` + zip + final checklist), `ai-usage-log` (keeps `docs/ai_usage.md` up to date; it feeds the mandatory generative-AI slide), `scikit-learn` (third-party, K-Dense; see below).
- Global: `skill-scout` (look for a better skill before a non-trivial task), `data-scientist`, `mcp-builder`.

Skills assigned to agents (found with `skill-scout` on 2026-10-29):

| Agent | Preloaded (`skills:`) | Loaded on demand |
|---|---|---|
| `model-experimenter` | `scikit-learn` | `data-scientist` |
| `methodology-reviewer` | `scikit-learn` | `data:validate-data`, `data:statistical-analysis` |
| `chart-reviewer` | | `dataviz` |
| `slides-writer` | `ai-usage-log` | `anthropic-skills:pptx` |
| `deliverables-checker` | `submission-package` | |
| `notebook-runner` | | |

`scikit-learn` comes from `K-Dense-AI/claude-scientific-skills` (commit 5f2bc03, MIT/BSD-3). It was vetted: `SKILL.md` and both scripts read in full, the references scanned. Two changes were made on install: the `allowed-tools` pre-approval and a section telling the agent to add a self-citation to reports were removed. Nothing in the official marketplace covers ML. Rejected: TabPFN (sends data to an external service, not allowed for student health data).

## Generative-AI disclosure

The brief makes us declare how we used generative AI. Whenever Claude writes or changes code, proposes an approach or drafts text for the project, append a line to `docs/ai_usage.md` (use the `ai-usage-log` skill). Never present AI-written work as hand-written, and never invent entries for work Claude did not do.
