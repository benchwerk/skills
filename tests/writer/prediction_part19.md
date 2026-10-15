# Part 19: does a skill for writing skills produce skills that get picked? Predictions

**Written 2026-10-09, before any run.** Committed with the hashes of the tasks, the runner and the skill under test (`inputs_hashes.json`).

## Question

`skill-writer` (in `skill-writer/`, committed 2026-10-09) is a skill that carries the rules measured in Parts 16 to 18: describe the situation in the user's words, no commands in the description, a descriptive name, a short body, only files that exist, manual-only for rarely used skills, run the audit script, test that it fires.
Does a skill written with it get picked more often than one written by plain Claude or with Anthropic's `skill-creator`?

## Design

10 requests (`part19_tasks.json`): five *task* skills (branch name from a ticket, explain a traceback, reply to an unclear bug report, README getting-started, cURL to Python requests) and five *process* skills (verify before saying done, confirm before destructive actions, failing test first, plan before a big change, stop when a command fails). Each request is given to Sonnet 5.5 in the same words in every arm:

> Write a Claude Code skill: <request> Save it as out/<slug>/SKILL.md (the folder out/ exists). Do not ask questions. Do not run the claude command.

Arms: `plain` (nothing installed besides the bundled skills), `creator` (Anthropic's `skill-creator` installed), `writer` (`skill-writer` installed, asked in the plain words, so it has to be picked by its own description), `writer-forced` (`skill-writer` installed and the request starts with `/skill-writer`).
One generation per request and arm: 40 skills. Each generated skill is then installed alone and tried on its four should-trigger and four near-miss requests (one run each; material inside; the prompts are fixed in the tasks file): 320 calls, each stopped at the model's first decision. The audit script is run on every generated skill. The prompts were written before any skill was generated, from the request only.

## Predictions

- **W1.** In the arm `writer` (not forced), `skill-writer` is called in at least 6 of 10 requests. In `creator`, `skill-creator` is called in at least 4 of 10.
- **W2.** Process skills, should-trigger prompts (20 per arm): the pooled skills of `writer` and `writer-forced` are called in at least 20 points more of the prompts than those of `plain`.
- **W3.** Task skills (20 per arm): `writer` and `writer-forced` within 10 points of `plain` (task skills are an easy case for plain Claude).
- **W4.** False triggers on the near-miss prompts: at most 10% in every arm (pooled over task and process skills, 40 prompts per arm).
- **W5.** Audit (independent of how the skill was written): the 20 skills of `writer` and `writer-forced` have no ERROR and at most 0.5 WARN each on average; the skills of `plain` have at least 1.0 WARN each on average.
- **W6.** Median description length: `writer` and `writer-forced` at most 300 characters, and shorter than `plain`'s.
- **W7.** Generation cost: output tokens per generation in `writer` and `writer-forced` at most 2 times those of `plain`.

## Verdicts and limits

As in the other parts. With 20 should-trigger prompts per arm and type, only differences of about 30 points are resolved; the generation is one sample per request and arm. The audit script and `skill-writer` encode the same rules, so W5 measures whether the writer follows its own rules, not whether the rules are right; W2 to W4 are the independent test.
One model and version, ten requests, print mode, a skill folder written in `out/` and installed afterwards. The tests inside `skill-writer` (steps 6 and 7) are limited: the run may not call `claude`.
