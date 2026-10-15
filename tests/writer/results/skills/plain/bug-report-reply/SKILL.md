---
name: bug-report-reply
description: Draft a polite, friendly reply to a bug reporter whose report is missing the details needed to reproduce the problem. Use when the user pastes or points to a bug report/issue that lacks steps, versions, environment, expected vs. actual behavior, logs, or a minimal example, and wants a response asking for them.
---

# Bug report reply

Draft a reply that thanks the reporter and asks for exactly the missing information, so they can answer quickly without feeling criticized.

## Steps

1. **Read the report** (pasted text, file, or issue URL/number the user gave). If it is an issue link and you can fetch it, do so; otherwise work from what was provided.
2. **Check what is already there.** Look for each of these:
   - Steps to reproduce (numbered, starting from a clean state)
   - Expected behavior vs. actual behavior
   - Version of the software (and relevant dependencies)
   - Environment: OS, browser/runtime, hardware, config, deployment type
   - Error messages, stack traces, logs, screenshots
   - Frequency (always, intermittent, once) and when it started (a regression?)
   - Minimal example, repro repo, or sample input, when relevant
3. **Pick only what is missing and actually needed** for this bug. Do not paste a generic checklist; a UI glitch needs a browser and screenshot, a crash needs a stack trace and version. Ask for at most 3-5 items, most useful first.
4. **If the project has an issue template or CONTRIBUTING guide**, check for it and point to it where relevant rather than inventing requirements.
5. **Write the reply** using the structure below.

## Reply structure

- **Thanks**: one sentence thanking them for reporting, specific to their issue where possible (show you read it).
- **What we understood**: one sentence restating the problem, so they can correct a misreading.
- **What we need**: a short list of the missing items. For each, say briefly what to provide and, where helpful, how (e.g. the command to print the version, where logs live).
- **Why / next step**: one line saying this lets you reproduce and fix it, and that you'll look into it once you hear back.

## Tone and style

- Warm, respectful, and concise. Assume good faith; never imply the reporter did something wrong.
- Say "could you share..." / "it would help to know...", not "you forgot..." or "you failed to...".
- No blame, sarcasm, or boilerplate-sounding corporate language. Avoid threatening to close the issue; if the user wants a stale-issue note, add a gentle one (e.g. "if we don't hear back we may close this for now, but you're welcome to reopen it").
- Match the language of the report. Keep it short enough to read in under a minute.
- Use plain Markdown that renders well in GitHub/GitLab/Jira comments.
- Don't promise a fix or timeline. Don't speculate about the cause unless the user asked.

## Output

Give the draft reply in a single block ready to copy, followed by at most one line noting any assumption you made (e.g. "I assumed this is the desktop app; adjust if not"). Don't post or send anything; the user does that.

## Example

Report: "App crashes when I open settings. Please fix."

Reply:

> Hi, and thanks for reporting this! It sounds like the app crashes when you open the Settings screen, which is definitely not what should happen.
>
> To help us reproduce it, could you share:
>
> 1. **App version and platform** (e.g. 2.4.1 on Windows 11), found under Help > About.
> 2. **Steps** you took from launching the app until the crash. Does it happen every time?
> 3. **Any error message or crash log**, if one appears.
>
> With that we should be able to track it down. Thanks again for your help!
