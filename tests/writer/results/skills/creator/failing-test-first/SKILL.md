---
name: failing-test-first
description: Use when fixing a bug, regression, or unexpected behavior. Write a test that reproduces the bug and confirm it fails for the right reason before changing any production code, then fix and confirm it passes.
---

# Failing Test First

When asked to fix a bug, do not touch production code until a test reproduces it and you have seen that test fail for the right reason.

## Workflow

1. **Understand the bug.** Read the report, error, or stack trace. State the expected behavior and the actual behavior in one sentence each. If you cannot, investigate more before writing anything.

2. **Find where the test belongs.** Locate the existing test file and conventions (framework, naming, fixtures, how tests are run) for the code under suspicion. Match them. Only create a new test file if none fits.

3. **Write the smallest test that reproduces the bug.** It should:
   - Exercise the real code path from the report, with the inputs that trigger it.
   - Assert the *correct* behavior (what should happen), not the buggy behavior.
   - Have a name describing the behavior, e.g. `returns_empty_list_when_no_items_match`, not `test_bug_123`.
   - Avoid mocking away the code that contains the bug.

4. **Run it and watch it fail.** Run only that test, using the project's runner. Do not skip this step or assume the result.

5. **Confirm it fails for the right reason.** Read the failure output and check:
   - The assertion fails with an actual value that matches the reported bug (wrong value, wrong exception, missing result), or the exception is the one reported.
   - It is NOT failing because of a typo, import error, missing fixture, syntax error, wrong test setup, or an unrelated exception.
   - If it failed for the wrong reason, fix the test and rerun until the failure matches the bug. Do not proceed on a wrong-reason failure.
   - If it *passes*, the test does not reproduce the bug. Revisit the reproduction (inputs, environment, path) rather than proceeding. If the bug truly cannot be captured in a test, say so explicitly and explain why before fixing.

   Report to the user briefly: the test name, the command run, and the failure message, with a note on why it matches the bug.

6. **Fix the bug.** Make the minimal production change that addresses the root cause. Do not edit the test to make it pass.

7. **Run the test again and confirm it passes.** Then run the surrounding test suite (at least the affected file or module) to check for regressions. Report results honestly; if anything fails, say so and resolve it.

## Rules

- No production edits before step 5 is complete.
- One bug, one failing test first. For several bugs, repeat the cycle per bug.
- Keep the new test in the codebase as a regression test.
- If the project has no test setup, set up the lightest-weight one that fits the language, or write a minimal standalone repro script that fails with a clear message, and tell the user.
