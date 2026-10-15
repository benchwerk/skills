---
name: stop-when-a-command-fails
description: When a shell command, build, test, or script fails (non-zero exit, error output, timeout), stop and report to the user instead of retrying blindly or working around it. Use whenever a command you ran returns an error.
---

# Stop when a command fails

When a command fails, do not keep going. Stop, report what happened, and let the user decide the next step.

## What counts as a failure

- A non-zero exit code
- Error, exception, or traceback output, even if the exit code is 0
- A timeout, a hang, or a killed process
- A permission denial or a refused tool call
- Output that contradicts what the command was meant to do (for example, "0 files changed" after an edit script)

## What to do

1. **Stop.** Do not run another command that tries to get past the failure.
2. **Read the output.** Take the exact error message from the output. Do not guess at it.
3. **Report to the user**, briefly, in this order:
   - The command you ran, verbatim
   - The exit code, if there is one
   - The relevant error output, quoted exactly. Trim noise but keep the actual error lines.
   - What you were trying to accomplish
   - What has and has not been done so far, including any partial side effects (files written, packages installed, migrations half-applied)
   - Your best read of the likely cause, labelled as a hypothesis if you haven't verified it
   - One or two options for what to do next, with a recommendation
4. **Wait** for the user's answer before you continue.

## What not to do

- Do not re-run the same command hoping it works. A single re-run is fine only if the output shows a clearly transient cause, and you say so in the report.
- Do not switch to a different tool, flag, or approach that sidesteps the failure. Examples: adding `--force`, `--no-verify`, or `--legacy-peer-deps`; using `sudo`; deleting a lock file or cache; disabling a test; editing the check so it passes.
- Do not continue with later steps that depend on the failed one.
- Do not hide the failure with `|| true`, `; exit 0`, `2>/dev/null`, or by ignoring the exit code.
- Do not claim success or summarize the task as done when a step failed.

## Read-only diagnosis is allowed

You may run read-only commands that explain the failure and change nothing. Examples: `git status`, `ls`, reading a log file, `--version`, or viewing the config. Include what you find in the report. Do not run anything that changes state as part of diagnosing.

## Exceptions

- If the user has told you in advance how to handle a specific failure ("if the lint step fails, just continue"), follow that instruction for that failure only.
- A command whose failure is the expected result (for example, a test you are writing that should fail first) is not a failure to report. Say that it failed as expected.

## Example report

> `npm test` failed with exit code 1.
>
> ```
> FAIL src/auth.test.ts
>   ● login › rejects expired token
>     Expected: 401
>     Received: 200
> ```
>
> I was running the suite after changing token validation in `src/auth.ts`. That edit is applied, and nothing else has been changed.
>
> Likely cause (unverified): my change skips the expiry check when `exp` is missing.
>
> Options: (1) I fix the expiry check and re-run the tests, which I'd recommend; (2) I revert the edit. Which would you like?
