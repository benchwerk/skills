---
name: verify-before-done
description: Use when you are about to tell the user a coding task (feature, fix, refactor) is done. Verify before done: run the tests and read the diff first. Do not use for questions, explanations or tasks with no code changes.
---

# Verify before done

Before you say a coding task is done, check the work.

1. Find the test command (package.json scripts, Makefile, pytest/tox config, CI file, README). Do not guess if one is documented.
2. Run the tests that cover the change, then the full suite if it is quick. Read the output, not just the exit code.
3. Run `git diff` (and `git status` for new files). Read every hunk.
4. Check the diff against the request:
   - Does it do what was asked, and nothing extra?
   - Leftover debug prints, commented-out code, TODOs, stray files?
   - Edge cases, error paths and callers of changed functions?
   - Did you change or delete a test just to make it pass?
5. Fix what you find, then repeat steps 2-3.
6. Report.

## Rules

- Do not say "done", "fixed" or "works" without a test run you saw pass in this session.
- Do not claim tests passed if you did not run them. If there are no tests or you cannot run them, say so and say what you checked instead.
- Do not hide failures, skipped tests or warnings you caused.
- Do not weaken or skip tests to get green.

## Output

Two or three lines: the command run and its result (pass/fail counts), what the diff covers, and any known gaps or things not verified.
