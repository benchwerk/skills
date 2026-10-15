---
name: bug-report-reply
description: Use when the user asks for a reply to a bug report or issue that lacks details to reproduce it (steps, version, environment, logs). Drafts a polite request for the missing info. Not for fixing bugs or triaging complete reports.
---

# Bug report reply

Draft a short, friendly comment asking a reporter for what is missing to reproduce their problem.

## Steps

1. Read the report (pasted text, issue file, or link content the user gave). If it is not available, say so; do not invent its contents.
2. List what is already given, so you never ask for it again.
3. Find what is missing. Check, in this order:
   - steps to reproduce, and what they expected versus what happened
   - version of the software, and OS / browser / runtime
   - exact error message, stack trace or log output
   - config, input or sample data that triggers it
   - how often it happens (always, sometimes, once) and whether it worked before
4. Keep only the 2-4 items that matter most for this report. Skip any that are irrelevant to it.
5. Write the reply.

## Rules

- Thank the reporter for the report first, in one sentence.
- Say why the details help ("so we can reproduce it"), once.
- Ask as a short numbered list, one question per item, with a concrete example of the format where useful (e.g. "the output of `app --version`").
- Mention what you already understood, so they see it was read.
- Do not blame, scold, or say the report is "incomplete" or "low quality".
- Do not promise a fix or a timeline.
- Do not guess at the cause or suggest a fix unless the user asks.
- Do not ask for secrets; tell them to redact tokens, passwords and personal data from logs.
- Match the language of the report. Keep it under about 150 words.

## Output

Only the draft comment, ready to paste, followed by one line to the user noting anything you assumed (for example, an unavailable attachment).

Example shape:

> Thanks for reporting this! I understand that the export fails on large files. To reproduce it, could you share:
> 1. The version (`app --version`) and your OS
> 2. The exact error message or log output (please redact any secrets)
> 3. The steps you took, or a small file that triggers it
>
> With that we can try it on our side.
