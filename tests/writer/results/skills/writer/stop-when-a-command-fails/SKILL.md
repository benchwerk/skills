---
name: stop-when-a-command-fails
description: Use when a command, build, test run, script or tool call you ran fails or exits non-zero. Stop and report the failure to the user instead of retrying or working around it. Do not use for expected non-zero exits.
---

# Stop when a command fails

A failed command is information for the user. Report it; do not paper over it.

## Steps

1. Stop at the first failure. Do not run the next step, even if it looks independent.
2. Re-read the output. Note the exact command, working directory, exit code and the key error lines.
3. Tell the user, in this order:
   - what you were trying to do;
   - the exact command and its exit code;
   - the relevant error text, quoted (trim noise, keep the first real error);
   - your best guess at the cause, labelled as a guess;
   - one or two options for what to do next, with your recommendation.
4. Wait for the user to choose. Do not act on the options yourself.

## Rules

- Do not retry the same command, with or without small changes (flags, sleeps, `--force`, `|| true`).
- Do not switch to a different tool or route that gets the same result (another package manager, manual file edits instead of the failed script, a different shell) without being asked.
- Do not hide the failure: no `2>/dev/null`, no ignoring exit codes, no skipping or deleting the failing test, no weakening checks.
- Do not make changes to "fix" the environment (installing, upgrading, deleting caches, changing permissions or config) unless the user asked for it.
- Do not report partial work as done. Say which steps finished and which did not.
- Read-only diagnosis is fine and encouraged to make the report better (view the log, check the path, print a version). Keep it to what is needed for the report.
- Exception: if the user said the failure is expected, or told you what to do on failure, follow that.

## Output format

**Command failed:** `<command>` (exit `<code>`, in `<dir>`)
**Goal:** one line
**Error:** quoted lines
**Likely cause (guess):** one line
**Options:** 1. ... 2. ... (recommended: N)
**State:** what completed and what did not
