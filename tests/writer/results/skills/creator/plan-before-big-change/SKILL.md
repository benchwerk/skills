---
name: plan-before-big-change
description: Before making a change that will edit, create, delete, or rename more than three files, state a three-line plan first. Use whenever a task (refactor, rename, feature, migration, bulk fix) is about to touch four or more files.
---

# Plan before a big change

Before you modify more than three files, stop and state your plan in exactly three lines. Then proceed.

## When this applies

Count every file you expect to edit, create, delete, or rename in the task. If the count is **four or more**, state the plan before making the first change. If it is three or fewer, skip this skill and just do the work.

If you start with a small change and discover mid-task that it will grow past three files, pause and state the plan at that point, before touching the fourth file.

Reading or searching files does not count. Only changes do.

## The plan format

Write exactly three lines, in this order:

1. **Goal:** what the change accomplishes, in one sentence.
2. **Files:** the files or groups of files you will touch (name directories or patterns if there are many) and the approximate count.
3. **Approach:** how you will do it, including the order of steps and how you will verify it (tests, build, grep).

Example:

```
Goal: Rename `getUser` to `fetchUser` across the API client.
Files: src/api/client.ts, src/api/index.ts, 6 call sites under src/pages/, and 2 test files (~10 files).
Approach: Rename the definition and re-export, update call sites with a search pass, then run the type check and test suite.
```

## Rules

- Exactly three lines. No preamble, bullets, or extra paragraphs in the plan itself.
- Put the plan in your visible response text, right before the first edit, not in your head.
- Do not wait for approval unless the user asked you to or the change is destructive (deleting data, force-overwriting, anything hard to reverse). In those cases, ask for confirmation after stating the plan.
- If the user has already given a detailed plan for this exact change, restate it in three lines rather than inventing a new one.
- If the plan changes materially during the work, state the revised plan in three lines before continuing.
