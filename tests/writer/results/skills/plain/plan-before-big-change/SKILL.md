---
name: plan-before-big-change
description: Before modifying, creating, deleting, or renaming more than three files in one task, state a three-line plan first. Use for refactors, renames, migrations, feature additions, and any multi-file edit.
---

# Plan Before Big Change

When a task will change **more than three files**, state a three-line plan before making the first edit.

## What counts

- Count every file you will edit, create, delete, or rename for the task, not just the first batch.
- Generated files, lockfiles, and formatter-only changes don't count unless you edit them by hand.
- If you are unsure whether the total will pass three, estimate with search (Grep/Glob) first. If it might, write the plan.
- If you discover mid-task that the count will exceed three, stop and write the plan before the next edit.

## The plan

Output exactly three lines, in this order, before any edit:

```
Goal: <what will be different when done, in one sentence>
Files: <the files or directories to be changed, grouped; say how many>
Approach: <the order of steps and how you'll verify, in one sentence>
```

Rules:

- Exactly three lines. No bullets, headers, or extra commentary around them.
- Each line is a single sentence, concrete enough that the user could spot a wrong assumption.
- Name real paths found by looking at the code, not guesses.

## After the plan

- Continue with the work right away. Do not wait for approval or ask questions, unless the user asked you to confirm first.
- If the plan changes materially (new files, different approach), state a revised three-line plan before continuing.
- Skip the plan for changes touching three files or fewer.

## Example

```
Goal: Rename `fetchUser` to `getUser` everywhere so the API naming is consistent.
Files: 7 files: src/api/user.ts, 4 callers under src/pages/, and 2 tests under tests/.
Approach: Rename the definition first, update callers and tests, then run the type-check and test suite.
```
