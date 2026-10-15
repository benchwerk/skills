---
name: stop-when-a-command-fails
description: When a shell command, build, test run, script, or other tool call fails (non-zero exit, error output, timeout, permission denied), stop and report the failure to the user instead of retrying blindly, changing approach, or working around it. Use whenever a command fails during any task.
---

# Stop When a Command Fails

A failed command is information the user needs. Do not hide it by retrying or routing around it. Halt, report, and let the user decide.

## When this applies

Any command or tool call that:

- exits non-zero, or prints an error, traceback, or "fatal"/"failed" message
- times out, is killed, or is denied (permissions, sandbox, missing credentials)
- reports success but clearly did not do the requested thing (e.g. zero tests ran, empty output where output was required)

## What to do

1. **Stop.** Make no further tool calls that continue the task. Do not run the next step of a plan.
2. **Report** concisely:
   - The exact command that was run (and working directory if relevant)
   - The exit code and the key error lines, quoted verbatim, not paraphrased
   - What you were trying to accomplish with it
   - What has already been done and is now in a partial state (files changed, installs done, services started)
3. **Give a likely cause only if the output supports it.** Label it as a hypothesis. Do not guess beyond the evidence.
4. **Offer options, then wait.** For example: fix X and rerun, try Y instead, skip this step, or the user handles it. Recommend one if you have a basis, but do not act on it without the user's go-ahead.

## What not to do

- Do not rerun the same command hoping it works ("flaky" is a conclusion for the user to draw, not you).
- Do not retry with `--force`, `sudo`, `-f`, `--no-verify`, disabled checks, or other flags that bypass the failure.
- Do not substitute a different tool, path, version, or method to get the same result without being asked.
- Do not delete files, caches, lockfiles, or state to "clear" the error.
- Do not edit code or config to make the failure disappear (silencing a test, loosening a check, stubbing a call).
- Do not continue with later steps that depend on the failed one, and do not claim the task is complete.
- Do not downplay the failure or bury it at the end of a long summary. Lead with it.

## Narrow exceptions

- **Diagnosis is fine.** Read-only commands to understand the failure (reading the log file mentioned in the error, `git status`, checking a version) are allowed, once, to make the report more useful. Do not use them as a backdoor to fix things.
- **The user pre-authorized it.** If the user explicitly said to retry or handle a specific failure (e.g. "retry up to 3 times", "if lint fails, auto-fix"), follow that instruction, but only for that failure and within those limits. Stop and report when the limit is hit or a different failure occurs.
- **Expected non-zero exits.** Commands where non-zero is the normal signal (e.g. `grep` finding no match, `diff` finding differences) are not failures unless the result is unexpected for the task. If unsure, treat as a failure and ask.

## Report template

```
Stopped: a command failed.

Command: <command>
Exit code: <n>
Error:
  <verbatim key lines>

Goal: <what this step was for>
State: <what has/hasn't been changed so far>
Possible cause: <hypothesis, if evidence supports one>

How would you like to proceed?
  1. <option>
  2. <option>
```
