# Skills: managing many, getting them picked, writing them

Follow-up tests on Claude Code skills, continuing the study
[skill-context-cost](https://github.com/benchwerk/skill-context-cost) (Parts 1 to 15 there; Parts 16 to 19 here).
Every number in these documents comes from a raw file in this repository. Measured with Claude Code 2.1.284 and 2.1.286
in print mode (`claude -p`), mostly on Sonnet 5.5, on one x86 laptop, 2026-10-08 and 2026-10-09.

## What is here

| Folder | What it holds |
| :-- | :-- |
| `skills/` | the suite: 15 generic developer-workflow skills written for these tests (see `SUITE.md`) |
| `skill-writer/` | a skill for writing skills, tested in Part 19 |
| `tests/manage/` | Part 16, managing many skills: what Claude sees of a long list, the description budget, manual-only skills, similar descriptions, documented settings, a version canary (`RESULTS.md`) |
| `tests/deep-think/` | Parts 17 and 18: a process skill for careful coding, and which description makes Claude call it (`RESULTS.md`) |
| `tests/writer/` | Part 19: does a skill for writing skills produce skills that get picked? (`RESULTS.md`) |

Each test folder holds its harness, its predictions (committed before the runs), the raw results under `results/`, the
analysis script and `RESULTS.md`.

## What was found

- **A version canary.** One skill's listing (`changelog-entry`) adds 76 tokens to the first request; the 15 suite skills
  together add 1,165 (`tests/manage/canary_2.1.284.json`, `tests/manage/canary_2.1.286.json`).
- **`disableBundledSkills: true`** in the project settings removed 14 of the 17 bundled skills and kept the project's
  own; the first request fell from 19,338 to 17,204 tokens (one call each; `tests/manage/results/m5/observations.json`).
- **The more skills are installed, the fewer get a description**, and manual-only skills take no part of that budget
  (Part 16, M2c and M2d).
- **When the description is cut off, the name alone decides** whether a skill is picked (Part 16, M2b).
- **A process skill almost never runs on its own:** a careful-coding skill was called in 0 of 96 plain coding runs
  across four skill arms; forced with a slash command, it fixed the second instance of a planted bug in 13 of 24 runs
  against 0 of 24 without a skill (Part 17).
- **The description decides whether it is called:** a description that names what the user says ("reports a bug, an
  error or a failing test") was called in 22 of 24 runs; "Always call this skill before editing any code." was ignored
  in 24 of 24 (Part 18).
- **A skill for writing skills** did not make the written skills get picked more often, and it cut the output tokens of
  writing one by 21% (1,486 against 1,876); asked for in plain words it was called in 10 of 10 requests, while the
  installed `skill-creator` was called in 0 of 10 (Part 19).

## Limits

Print mode only; one machine; mostly one model and one or two Claude Code versions; small samples (one to three runs per
cell in Part 16, 24 runs per arm in Parts 17 and 18, one run per prompt in Part 19). Treat the numbers as a guide to
what to expect, not as a promise. Each `RESULTS.md` lists its own caveats.

The skills under test in Parts 17 and 18 (`deep-think` in two versions, and a completed variant) are not published;
their SHA-256 hashes are recorded in `tests/deep-think/inputs_hashes*.json`.

## Reproduce

The harnesses call Claude Code (`claude -p`) in an isolated configuration folder and need a Claude login; each test's
`RESULTS.md` names its script, its run folder and its analysis script. The analysis scripts read only the raw files in
`results/` and rewrite the `*_findings.json` next to them.

## Licence

Code (harnesses, analysis scripts, the skills): MIT, see `LICENSE`. Data and documents: CC BY 4.0, see `LICENSE-DATA`.
