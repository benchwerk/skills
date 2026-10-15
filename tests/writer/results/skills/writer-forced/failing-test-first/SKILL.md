---
name: failing-test-first
description: Use when the user reports a bug, an error, a crash or wrong output and wants it fixed. Writes a test that reproduces it, confirms it fails for the right reason, then fixes. Do not use for new features or refactors.
---

# Failing test first

1. Restate the bug in one line: input, expected result, actual result. If the report lacks this, infer it from the code and error text.
2. Find the existing test setup (framework, test folder, naming, run command). Put the new test next to similar tests and match their style.
3. Write the smallest test that triggers the bug and asserts the expected behavior. Do not touch the production code yet.
4. Run only that test. It must fail.
5. Check the failure is the right one:
   - The failure message shows the actual wrong value, or the same exception, as the report.
   - It is not an import error, typo, missing fixture, wrong path, or setup error.
   - The assertion would pass if the bug were absent.
   If it fails for another reason, fix the test and rerun. If it passes, the test does not reproduce the bug: change the input or setup until it fails, or tell the user the bug was not reproduced.
6. Show the user the failing output in one or two lines and say why it is the right failure.
7. Fix the production code with the smallest change that addresses the cause.
8. Rerun the new test (must pass), then the surrounding test file or suite (must not break).

## Rules

- Do not edit production code before step 4 has shown a failing run.
- Do not weaken, skip, or delete a test to make it pass.
- Do not write a test that asserts the buggy behavior.
- Do not fix other things you notice; mention them instead.
- If the project has no test framework or the bug cannot be tested (UI timing, external service), say so and use the closest repeatable check, such as a script that exits non-zero.

## Output

Report: the test file and name, the failing output (before), the change made, and the passing output (after). Say plainly if any step was not run.
