# Part 18: what makes Claude call a process skill? Predictions

**Written 2026-10-09, before any run of these arms.** Committed with `inputs_hashes_after_part18.json`. Follows `RESULTS.md` (Part 17): the skill `deep-think` was almost never called on its own (0 of 96 plain coding runs, 6 of 96 with "Please be thorough.").

## Question and design

Same skill body (V3 complete), same 12 plain coding tasks (each a bug report), same Sonnet 5.5 and Claude Code 2.1.286. Only the `description` line changes (`description_variants.py`, hashed):

| Arm | Description |
| :-- | :-- |
| d0 | exactly as received (the control; "Makes Claude work thoroughly ... Use for ANY non-trivial task ...") |
| d1 | names the task: "Use at the start of any coding task that changes files: fixing a bug, adding a feature, refactoring ..." |
| d2 | names what the user says: "Use when the user reports a bug, an error or a failing test ..." |
| d3 | names the moment: "Use before telling the user that a coding task is done, to verify the work ..." |
| d4 | the original, plus "Always call this skill before editing any code." |

Runs: 12 coding tasks x 5 arms x 2 = 120. To measure false triggers, 4 general prompts that are not bug reports (`trivial-a`, `trivial-b`, `message-a`, `helpfirst-a`) x 5 arms x 2 = 40. In all: 160. Measures: skill called (a Skill tool call), second instance fixed, output tokens, turns.

## Predictions

- **P18.1.** d0 is called in at most 10% of the 24 coding runs (the main run gave 0%).
- **P18.2.** d2 is called in at least 75%; d1 and d4 in at least 60% each.
- **P18.3.** d3 is called in at least 30%, and at least 15 points less often than d2 (Claude has to decide at the end of the work).
- **P18.4.** Pooled over the five arms, runs where the skill was called fix the second instance at least 20 points more often than runs where it was not (if at least 15 runs called it).
- **P18.5.** Runs where the skill was called use at least 1.5 times the output tokens of runs where it was not.
- **P18.6.** False triggers on the four non-bug prompts (8 runs per arm): d1, d2 and d3 at most 1 of 8; d0 and d4 at most 2 of 8.
- **P18.7.** The arm with the highest call rate on the coding tasks is d2 or d4.

## Verdicts and limits

As in `prediction.md`: *holds* when every clause is met on the point estimate; intervals are reported. With 24 coding runs per arm and 8 false-trigger runs per arm, differences below about 25 points are not resolved.
One model, one version, one skill, bug-report prompts only, print mode. Nothing here shows that the winning description works for other skills; it shows what changed for this one.
