---
name: plan-before-big-change
description: Use when a task or request will make you edit, create, rename or delete more than three files (refactors, renames, migrations, new features). States a three-line plan first. Do not use for changes to three files or fewer.
---

# Plan before a big change

1. Before the first edit, count the files you expect to change, create, rename or delete. Include tests, configs and docs. Reading files does not count.
2. If the count is three or fewer, skip this skill and work normally.
3. If it is more than three, write exactly three lines before touching anything:
   - `Goal:` what will be different when you are done.
   - `Files:` the count and the main files or folders, grouped if many.
   - `Order:` the steps in the order you will do them, and how you will check them.
4. Then continue with the work in the same turn. Do not wait for approval unless the user asked for it or the change is destructive (deleting files, rewriting history).
5. If the count grows past your stated plan while working (a new area, a surprise dependency), write a new three-line plan before going on.

## Rules

- Exactly three lines. No headings, no bullets inside a line, no extra paragraph.
- Do not edit any file before the plan is written.
- Do not pad the plan with guesses. If you do not know the count, search first, then state it.
- Do not write the plan for small changes.

## Output format

```
Goal: <one sentence>
Files: <N> files — <main files or folders>
Order: <step 1> → <step 2> → <step 3>; verify with <test or check>
```
