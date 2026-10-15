---
name: failing-test-first
description: Use when fixing a bug, regression, or unexpected behavior. Requires writing a test that reproduces the bug and fails for the right reason BEFORE changing any production code, then making it pass with the fix.
---

# Failing Test First

When asked to fix a bug, do not touch production code until a test has reproduced it. A test that has never been seen failing proves nothing: it may pass for the wrong reason, or never exercise the bug at all.

## Workflow

### 1. Understand the bug
- Restate the expected behavior vs. the actual behavior in one or two sentences.
- Find the code path involved and the project's existing test setup (framework, location, naming, how to run a single test). Follow its conventions.
- If the bug cannot be reproduced from the report, gather more information (logs, inputs, git history) rather than guessing.

### 2. Write the test
- Write the smallest test that exercises the buggy behavior through the public interface (or the lowest level where the bug is observable).
- Assert the **correct** behavior, not the buggy one. The test should encode what should happen.
- Use a name that describes the behavior, e.g. `returns_empty_list_when_no_items_match`, and reference the issue number if there is one.
- Put it next to related tests. Do not edit production code in this step.

### 3. Run it and confirm it fails
- Run only this test and show the actual output.
- If it **passes**: the test does not reproduce the bug. Fix the test (wrong input, wrong layer, wrong assertion) or revisit your understanding of the bug. Never proceed to the fix with a passing test.

### 4. Confirm it fails for the right reason
Read the failure message and check it against the bug you were asked to fix. Explicitly state: "Failed because X, which matches the reported bug."

Wrong reasons (fix the test before continuing):
- Import/syntax/compile error, missing fixture, typo
- Setup or environment problem (missing DB, network, config)
- Calling a function or attribute that doesn't exist
- A different assertion failing than the one that captures the bug
- An unrelated exception raised before reaching the buggy line

Right reason: the code runs to the point of the bug and the assertion fails with the wrong value/behavior described in the report (e.g. `expected [], got None`).

### 5. Fix the bug
- Make the minimal change that addresses the root cause. Do not modify the new test to make it pass.
- No unrelated refactoring in the same change.

### 6. Verify
- Run the new test: it must now pass.
- Run the surrounding test suite (at least the affected file/module) to check for regressions.
- Report: the test added, the failure observed before the fix (and why it was the right failure), and the passing result after.

## Edge cases
- **No test infrastructure:** create the minimal setup needed, or if truly impossible, write a standalone reproduction script, show it failing, and say why a proper test wasn't feasible.
- **Hard-to-test bugs (UI, concurrency, timing):** reproduce at the nearest testable seam; make the test deterministic (inject clocks, fakes, seeds). Don't ship flaky tests.
- **Multiple bugs:** one failing test per bug, each confirmed separately.
- **Optional sanity check:** after the fix, temporarily revert it (e.g. `git stash` the production change) to confirm the test fails again, when cheap to do.
