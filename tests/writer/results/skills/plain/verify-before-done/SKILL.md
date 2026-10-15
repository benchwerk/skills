---
name: verify-before-done
description: Before saying a coding task is finished, complete, fixed, or ready, run the project's tests and read the full diff of your changes. Use at the end of any task that edited code, and before any "done" summary or commit.
---

# Verify before done

Do not tell the user a coding task is finished until you have run the tests and read your own diff. "Done" is a claim about the current state of the code, so check that state first.

## Steps

1. **Find the test command.** Check CLAUDE.md, README, `package.json` scripts, `Makefile`, `pyproject.toml`, `Cargo.toml`, CI config, etc. If none exists, use the closest check available (type check, linter, build, or running the changed code directly).
2. **Run the tests.** Run the full relevant suite, not only the test you wrote. For a large suite, run the affected tests first, then the broader suite if time allows. Also run the linter or type checker if the project has one.
3. **Read the diff.** Use `git diff` (plus `git status` for new untracked files). If the directory is not a git repo, re-read each file you changed. Read all of it, line by line, as a reviewer would. Look for:
   - Changes that don't belong: debug prints, commented-out code, stray files, unrelated edits.
   - Missed requirements: reread the original request and tick off each part.
   - Bugs: off-by-one errors, unhandled errors or empty inputs, wrong variable names, leftover TODOs.
   - Unintended side effects: changed signatures or behavior that other callers depend on.
   - Secrets or local paths committed by accident.
4. **Fix and re-run.** If tests fail or the diff shows problems, fix them and repeat steps 2–3. Don't report done while anything is red.
5. **Report honestly.** In the final message state:
   - The exact command(s) you ran and the result (pass/fail counts).
   - What you found in the diff review, and anything you changed because of it.
   - Anything you could not verify (no tests exist, tests can't run here, a failure that predates your change) and why. Never imply tests passed if you did not run them.

## Rules

- Never claim success from memory or from having "just written" the code. Run it.
- Don't weaken, skip, or delete tests to make them pass. If a test is genuinely wrong, say so and explain.
- If a failure is pre-existing and unrelated, confirm it (e.g. by checking it fails without your change), then report it separately rather than hiding it.
- If no tests cover your change, add one when reasonable, or say plainly that the change is untested.
- Keep the check proportionate: for a one-line trivial edit, a quick targeted test and a glance at the diff is enough, but never skip both.
