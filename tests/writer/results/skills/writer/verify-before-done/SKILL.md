---
name: verify-before-done
description: Use when you are about to say a coding task (feature, bug fix, refactor) is done or finished. Verify first: run the tests and read the diff before reporting. Do not use for questions, explanations or tasks with no code changes.
---

# Verify before done

Do these before saying a coding task is done, fixed or working.

1. **Find the tests.** Check the project for how tests run (CLAUDE.md, package.json scripts, Makefile, pyproject, CI config). If you do not know, look; do not guess.
2. **Run them.** Run the tests that cover the change, then the wider suite if it is quick. Also run the linter, type check or build if the project has one. Read the actual output, not just the exit code.
3. **Read the diff.** Run `git diff` (and `git status` for new files; if there is no git repo, re-read each file you edited). Check that:
   - every change is intended and nothing unrelated slipped in;
   - no debug prints, commented-out code, TODOs or stray files are left;
   - the change really does what the user asked, including edge cases;
   - callers, other usages and docs affected by the change are updated.
4. **Fix and repeat.** If a test fails or the diff shows a problem, fix it and go back to step 2. Do not report done with a known failure.
5. **Report honestly.** State what you ran and the result, and what you changed.

## Rules

- Do not say "done", "fixed" or "should work" before steps 2 and 3 are finished.
- Do not skip, delete, or weaken a test to make it pass, unless the user asked.
- If there are no tests, say so, and verify another way (run the code, try the failing case) and report how.
- If tests cannot run (missing dependency, no access), say that plainly and say what is unverified.
- Do not claim a pre-existing failure is unrelated without checking it fails without your change.
- Do not paste long output; give the command, the pass/fail counts and any failures.

## Final message format

- **Changed:** one or two lines.
- **Verified:** command(s) run and result (for example `pytest: 42 passed`).
- **Diff review:** what you checked, any issues found and fixed.
- **Not verified:** anything you could not run or check, or "nothing".
