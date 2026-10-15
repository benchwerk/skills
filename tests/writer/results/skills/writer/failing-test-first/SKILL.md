---
name: failing-test-first
description: Use when the user reports a bug, an error, a regression or wrong output and wants it fixed. Writes a failing test first and confirms it fails for the right reason. Do not use for new features or refactors.
---

# Failing test first

Reproduce the bug in a test before changing any production code.

## Steps

1. **State the bug as one expectation**: "Given X, the code should return/do Y, but it returns/does Z." If the report is vague, infer it from the code and error text; do not stop to ask.
2. **Find the test setup.** Look for the existing test framework, test folder, naming and helpers. Put the new test next to the tests for the same module, in the same style.
3. **Write the smallest test** that exercises the bug through the public behavior. Name it after the behavior (`test_total_ignores_negative_discount`), not the ticket.
4. **Run only that test** and read the output. Do not touch production code yet.
5. **Check it fails for the right reason.** The failure must be the bug itself: the assertion fails with the wrong value (Z), or the reported error is raised. Compare the message with the user's report. These are the wrong reasons; fix the test and rerun:
   - import error, syntax error, missing fixture, typo in a name
   - the test passes (it does not reproduce the bug: change the input or setup until it does, or tell the user the bug did not reproduce)
   - it fails on a different assertion or error than the one reported
6. **Fix the bug** with the smallest change that addresses the cause.
7. **Rerun the new test** and see it pass, then run the rest of the test file or suite to check nothing else broke.
8. **Report** briefly: the test name, the failure message you saw before the fix, and the passing result after.

## Rules

- Do not edit production code before step 5 is done.
- Do not weaken or delete an existing test to make the new one pass.
- Do not mock the thing that is broken.
- Do not claim the test "would fail" without running it. If the tests cannot be run, say so and say what you could not confirm.
- If the project has no test setup and adding one is large, write the smallest runnable reproduction script instead, run it, and say that you did.
- One bug, one test. Add more tests only for separate cases of the same bug that you found.

## Output

Short summary:
- **Test:** file and name
- **Failed before fix with:** the actual message, and why it is the right reason
- **Fix:** one line
- **After:** result of the new test and of the wider run
