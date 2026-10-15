---
name: stop-when-a-command-fails
description: Use when a command, build, test run or script you ran fails (non-zero exit, error output, permission denied). Stop, report the failure and ask before retrying or working around it. Not for failures the user asked you to debug.
---

# Stop when a command fails

1. When a command exits non-zero or prints an error, stop. Do not run the next step.
2. Read the full output. Do not guess at the cause.
3. Report to the user:
   - the exact command and the directory it ran in
   - the exit code and the key error lines, quoted
   - what you think caused it, marked as a guess if unverified
   - what you had not yet done because of the stop
4. Offer one to three options (for example: fix the cause, retry as is, skip the step) and wait for the user to choose.

## Rules

- Do not retry the same command unchanged, in a loop or "just once more".
- Do not work around it: no switching tools, no disabling checks, no `--force`, `--no-verify`, `sudo`, or loosened permissions, no editing tests or config to make the error disappear.
- Do not carry on with later steps that depend on the failed one.
- Do not hide the failure in a summary or say "mostly done".
- Read-only checks to understand the failure (viewing a log, `--version`, listing a folder) are fine. Say what you ran.
- If the user has already told you how to handle this failure, follow that instead.

## Output format

**Command failed:** `<command>` (exit `<code>`)
**Error:** `<quoted lines>`
**Likely cause:** `<one sentence>`
**Not done yet:** `<remaining steps>`
**Options:** `<short list>`
