# Generative-AI usage log

Required for the final slides ("how you used generative AI models throughout the work"). Kept up to date with the `ai-usage-log` skill. Entries are factual.

| Date | Area | What the AI did | What the human did / decided |
|---|---|---|---|
| before 2026-10-29 | EDA (`01_eda`), project scaffolding | Not recorded | Ana committed the EDA notebook and figures; Tomas committed the project template (git history) |
| 2026-10-29 | Tooling/setup | Claude Code read the brief and the repo and wrote `CLAUDE.md`, six subagents (notebook runner, methodology reviewer, model experimenter, chart reviewer, slides writer, deliverables checker) and two project skills | The user asked for the environment and supplied the brief |
| 2026-10-29 | Tooling/setup | Claude Code searched for existing skills (marketplace and web), vetted and installed the `scikit-learn` skill with two edits, and assigned skills to the agents | The user asked for the skill search and assignment |
| 2026-10-29 | Tooling/setup | Claude Code wrote `docs/assignment.md` (the brief as a checklist) and `docs/assumptions.md` (open decisions), and linked them to `CLAUDE.md` and the agents | The user asked for both documents |
| 2026-10-29 | Features, tests | Claude Code wrote `src/miopia/features.py`, `src/miopia/plotting.py` and `tests/test_features.py` from the notebook 01 decisions, and corrected the feature code after a review found exact dependencies among the retinal columns | The user asked for it |
| 2026-10-29 | Report (notebook 02) | Claude Code wrote and executed `02_cleaning_features.ipynb` and the notebook template; two AI review agents (methodology and charts) checked it and their findings were applied | The user asked for it |
| 2026-10-29 | Review of notebook 01 | Two AI review agents (methodology and charts) reviewed `01_eda`; their findings were then applied by Claude Code (privacy of printed rows, figures, multiple-test correction, wording of claims) and the notebook was re-executed | The user asked for the review |
| 2026-11-01 | Decision B2 (inconsistent `MM` labels) | Claude Code explained the options, proposed the comparison design and two possible adoption rules (it recommended keeping the original labels by default), and recorded the decision in `docs/assumptions.md` and `CLAUDE.md` | Ana first chose to correct the labels by default, then, after seeing the notebook 03 comparison, decided to keep the labels as provided and report the correction only as a separate experiment |
| 2026-11-01 | Validation, report (notebook 03) | Claude Code wrote `src/miopia/validation.py`, proposed the bar for a clear difference (B12), wrote and executed `03_baselines_validation.ipynb`; two AI review agents (methodology and charts) checked it and their findings were applied | Ana asked for it |
| 2026-11-01 | Decisions B12 and B13 (model comparison rules) | Claude Code proposed both rules and recorded them | Ana confirmed both |
