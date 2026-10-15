---
name: pull-request-description
description: Use when the user asks for a pull request title or description, or to improve one, from a branch, diff or commit list. Do not use for single commit messages, changelog entries or release notes.
---

# Pull request description

Write a description a reviewer can act on.

1. Read the full diff and the commit list. Work out what the reviewer must look at first.
2. Title: under 70 characters, imperative, says what the change does.
3. Sections, in this order: Summary (2 to 4 sentences: what and why), Changes (a short list grouped by area), How it was tested, Risks and rollout, Review notes (where to start, what is deliberately left out).
4. Mark breaking changes and migrations clearly at the top of Summary.
5. If tests were not run, say so; do not write "tested" without evidence from the user.

Rules
- No line-by-line restatement of the diff.
- Link issues only if the user gave them.
- Keep it under about 300 words unless the change is large.

Output the title and the description in Markdown.
