# Part 19 results: does a skill for writing skills produce skills that get picked?

Run 2026-10-09 (generation in the afternoon, trigger tests after the 20:19 reset). Predictions committed 15:53:53 (`e0ec150`) before any generation. Raw data: `results/raw_gen.jsonl` (40 generated skills), `results/raw_trig.jsonl` (320 trigger calls), `results/skills/` (the skills themselves); scored with `analyze_part19.py` into `results/part19_findings.json`. **4 of 7 clauses hold, 3 fail.**

Ten requests (five task skills, five process skills) given in the same words to four arms; each written skill was installed alone and tried on four should-trigger prompts and four near-misses (material inside), one run each.

| Arm | Skills written | Task skills picked (20 prompts) | Process skills picked (20 prompts) | False triggers (40 prompts) | Median description | Audit warnings per skill | Output tokens per generation |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| plain Claude | 10 of 10 | 20 (100%) | 9 (45%, interval 25.8 to 65.8) | 0 | 247.5 characters | 0.3 | 1,876 |
| with `skill-creator` installed | 10 of 10 | 19 (95%) | 8 (40%) | 0 | 278.0 | 0.3 | 1,886 |
| with `skill-writer`, asked in plain words | 10 of 10 | 20 (100%) | 8 (40%) | 0 | 220.5 | 0 | 1,486 |
| with `skill-writer`, forced | 10 of 10 | 19 (95%) | 9 (45%) | 0 | 216.5 | 0 | 1,383 |

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| W1 `skill-writer` called in 6+ of 10 requests (asked in plain words); `skill-creator` in 4+ | `skill-writer` 10 of 10; `skill-creator` 0 of 10 | fails (because of `skill-creator`) |
| W2 process skills: writer arms 20+ points above plain | 42.5% against 45.0% | fails |
| W3 task skills: writer arms within 10 points of plain | 100% and 95% against 100% | holds |
| W4 false triggers at most 10% in every arm | 0 of 40 in every arm | holds |
| W5 audit: writer arms no error and at most 0.5 warning; plain at least 1.0 | writer 0 and 0; plain 0.3 | fails (plain already clean) |
| W6 median description at most 300 characters and shorter than plain | 220.5 and 216.5 against 247.5 | holds |
| W7 output tokens of the writer arms at most 2x plain | 1,486 and 1,383 against 1,876 | holds |

## What it shows
- **A skill that carries the writing rules did not make the written skills get picked more often.** The picked-rate of the process skills was 45%, 40%, 40% and 45% in the four arms. Plain Claude (Sonnet 5.5) already wrote what the rules ask for: a description that begins "Use when ..." or "Before saying ..." and names the situation, 0.3 warnings per skill on the audit script, no false triggers.
- **The difference between skills is the situation, not the writer.** Process skills tied to the request were picked in 4 of 4 prompts in every arm (`confirm-destructive-actions`: "delete the build folders", `failing-test-first`: "bug: ..., fix it"). Process skills tied to a moment in the middle of the work were picked in 0 or 1 of 4 in every arm: `verify-before-done` ("before saying a task is finished"), `stop-when-a-command-fails` ("when a command fails"), `plan-before-big-change` ("before changing more than three files"). Claude chooses skills from the user's request at the start; a skill whose trigger is something that happens later in the work is not chosen from the request, however well it is described. This agrees with Part 18, where the "before telling the user the task is done" description was called in 8.3% of runs.
- **`skill-writer` itself works as a delivery mechanism:** asked in plain words, it was called in 10 of 10 requests. `skill-creator`, installed but asked in plain words, was called in 0 of 10 (in Part 14E of the study skill-context-cost it ran only when forced with a slash command).
- **It made the writing cheaper:** 21% fewer output tokens than plain (1,486 against 1,876) and slightly shorter descriptions, without a loss in trigger rate.

## Caveats
- One generation per request and arm, 20 should-trigger prompts per arm and type: only differences of about 30 points are resolved. All four arms are inside each other's intervals.
- The prompts for the process skills were written from the request alone; three of the five process skills turned out to have a trigger in the middle of the work. That is a result about those skills, not a flaw to be repaired afterwards, and the arms are compared on the same prompts.
- `skill-writer` and the audit script encode the same rules, so W5 measures whether the writer follows its rules, not whether the rules are right; W2 to W4 are the independent test.
- One model (Sonnet 5.5), one version, print mode.
- Before publication (2026-10-15) one line of `run_part19.py` was changed: a local absolute path to the pinned `skill-creator` clone was replaced by the same path relative to the script. The hash in `inputs_hashes.json` is of the file as run.

## Change to `skill-writer` after the test
Before any further test, a rule was added to the draft (version 2, untested): if a skill's trigger is something that happens in the middle of the work (after finishing, when a command fails), do not rely on a skill; put the rule in `CLAUDE.md` (always on) or make the skill manual-only and call it by name. Whether the writer then steers users to the right mechanism is not yet measured.
