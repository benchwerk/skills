---
name: bug-report-reply
description: Draft a polite reply to a bug reporter whose report is missing details needed to reproduce the problem (steps, versions, environment, logs, expected vs actual). Use when the user pastes a bug report or issue and asks for a response, a follow-up, a request for more info, or says a report is vague, incomplete, or "can't reproduce".
---

# Bug report reply

Draft a short, friendly reply that asks the reporter for exactly the missing information, and nothing more.

## Process

1. **Read the report.** Note what is already provided: summary, steps, expected vs actual behavior, version, OS/browser/runtime, logs or screenshots, frequency.
2. **Identify the gaps that block reproduction.** Only include items that are truly missing and that would help here. Typical candidates:
   - Exact steps to reproduce, starting from a clean state
   - What they expected vs. what happened (exact error text)
   - Software version or commit, and how it was installed
   - OS, browser, runtime, or device details
   - Relevant config, input data, or a minimal example
   - Logs, stack trace, or screenshot/recording
   - How often it happens (always, intermittent) and whether it started after a change
3. **Check for project guidance.** If the repo has an issue template, CONTRIBUTING file, or a command for collecting diagnostics (e.g. a `--version` or `doctor` command), point to it and use its wording for the fields.
4. **Write the reply** using the structure below.

## Reply structure

- **Thanks** them for reporting, in one sentence. Be specific if they did something useful (e.g. included a screenshot).
- **Acknowledge** what you understood the problem to be, in one line, so they can correct you.
- **Ask** for the missing details as a short numbered list, at most 5 items. Each item says what is needed and, where it isn't obvious, how to get it (a command to run, where logs live). Put the most important item first.
- **Close** by saying what happens next ("With that we can try to reproduce it") without promising a fix or timeline.

## Tone rules

- Assume good faith. Never imply the reporter did something wrong or should have known better.
- Don't use canned bureaucratic phrasing ("Please fill out the template"); say what you need in plain words.
- Don't ask for things already in the report. Don't ask more than needed.
- Don't speculate about the cause or blame their setup.
- Keep it under roughly 150 words unless the commands you include need more.
- Match the language of the reporter, and the formatting of the platform (Markdown for GitHub/GitLab; plain text for email).

## Output

Give the draft reply ready to paste, followed by one line listing which gaps you asked about, so the user can adjust. If the report already contains enough to reproduce, say so instead of drafting a request, and suggest next steps (try reproducing, label, etc.).

## Example

Report: "App crashes when I open settings. Please fix."

Reply:

> Thanks for reporting this! It sounds like the app crashes as soon as you open Settings. To help us reproduce it, could you share:
>
> 1. The app version (Help → About) and your OS version
> 2. What you do right before the crash, step by step, starting from launching the app
> 3. The error message or crash log, if one appears (logs are in `~/.app/logs/`)
> 4. Whether it happens every time or only sometimes
>
> Once we have that we'll try to reproduce it on our side.
