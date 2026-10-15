---
name: plan-before-big-change
description: Use when the user asks for a change that will touch more than three files (a rename, refactor, migration, or feature across modules). States a three-line plan first. Do not use for edits to three files or fewer.
---

# Plan before big change

1. Work out which files the request will change. Search first if unsure; read-only searching needs no plan.
2. If the count is three or fewer, skip this skill and just do the work.
3. If it is more than three, write exactly three lines before the first edit:
   - Goal: what changes, in one sentence.
   - Files: how many files and which areas or folders.
   - Order: the steps in the order you will do them, and how you will check the result.
4. Then start the edits in the same turn. Do not wait for approval unless the user asked you to.
5. If the real count grows past what the plan said, write a new three-line plan before continuing.

## Rules

- Exactly three lines. Do not add a preamble, a closing summary or a fourth line.
- Do not list every file by name; name the areas.
- Do not plan for read-only work, questions or explanations.
- Do not count generated files, lockfiles or files you only read.

## Output format

```
Goal: <one sentence>
Files: <N files in a/, b/, c/>
Order: <step 1 -> step 2 -> step 3; check with <test or command>>
```
