---
name: ai-usage-log
description: Keeps docs/ai_usage.md, the honest record of how generative AI was used in the myopia ML project (needed for the mandatory AI-usage slide). Use after any work in which Claude wrote or changed code, proposed an approach, reviewed work or drafted text, and when preparing the AI-usage slide.
---

# ai-usage-log

The professor requires a slide stating how generative AI was used (code, ideas on how to proceed, etc.). This log is its only source, so it must be accurate and complete.

## After each work session
Append one row to the table in `docs/ai_usage.md`:

| Date | Area | What the AI did | What the human did / decided |
|---|---|---|---|

- **Area**: EDA, features, validation, models, charts, report text, slides, tooling/setup, review.
- **What the AI did**: concrete and specific (e.g. "wrote the `RepeatedStratifiedKFold` comparison code", "proposed using permutation importance", "reviewed notebook 03 for leakage"). Mention subagent reviews as AI work.
- **What the human did**: decisions, checks, edits, parts written by hand. If the user did not say, write `[ask the user]` rather than guessing.
- One line each, plain words, no number-packed detail.

## Rules
- Never delete or soften past entries. Never invent work Claude did not do, and never credit the AI for something the user did.
- Entries about the earlier notebook `01_eda` are unknown unless the user says how it was made: leave them as `[ask the user]`.
- Do not log any student data.

## For the slide
Summarise the table into 4-5 bullets grouped by area, with what was AI-assisted, what was reviewed by humans, and one sentence on how outputs were verified (execution, review agents, the user's own checks). Hand the bullets to `slides-writer`.
