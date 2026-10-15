---
name: verify-before-done
description: Before saying a coding task is finished, complete, fixed, or ready, run the project's tests and read the full diff of your changes. Use at the end of any task that modified code, including bug fixes, features, refactors, and config changes, before reporting the result to the user.
---

# Verify before done

Never report a coding task as finished on the strength of having written the code. Check it first, then report what you actually observed.

## Steps

1. **Find the test command.** Check the project docs (CLAUDE.md, README, CONTRIBUTING), then the manifests and config (package.json scripts, Makefile, pyproject.toml, Cargo.toml, go.mod, CI workflows). If you can't find one, say so rather than guessing.

2. **Run the tests.** Run the narrowest relevant tests first, then the broader suite if it's reasonably fast. Also run the linter, type checker, or build if the project has one. Read the actual output. Don't assume a pass.
   - If a test fails, find the cause and fix it, then rerun. Don't skip, delete, or loosen a test to get green unless the test is truly wrong, and tell the user if you did.
   - If a failure looks unrelated to your change, confirm it (for example, by checking whether it also fails without your change) and report it as pre-existing.
   - If there are no tests covering your change, add one when practical. Otherwise exercise the change directly (run the script, call the function, hit the endpoint) and report what you saw.

3. **Read the diff.** Use `git diff` (plus `git status` for new untracked files). If the directory isn't a git repo, reread each file you changed. Review it as a skeptical reviewer would:
   - Does every change belong to the task? Remove stray edits, debug prints, commented-out code, and leftover TODOs.
   - Does it do what was asked, including edge cases and error paths?
   - Were any files unintentionally modified, deleted, or left out (new files, config, docs, migrations)?
   - Are there secrets, hardcoded paths, or generated files that shouldn't be there?

4. **Fix and re-verify.** If steps 2 or 3 turned up problems, fix them and repeat both steps. The final test run must come after the final edit.

5. **Report honestly.** In your closing message state:
   - what you ran (commands) and the result (pass/fail counts);
   - what you reviewed in the diff and anything notable;
   - anything you could not verify (tests that can't run here, no test coverage, skipped checks) and why.

   If tests fail or you couldn't run them, say so plainly. Never claim "all tests pass" or "done" without having seen it. A partial result honestly stated beats a confident claim that's unverified.

## Notes

- Skip nothing because the change looks trivial; small edits break things too. For a docs-only change, reading the diff is enough and tests can be skipped, but say so.
- Don't commit, push, or take other outward-facing actions as part of verification unless the user asked.
