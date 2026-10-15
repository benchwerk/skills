---
name: commit-message-format
description: Use when the user asks for a git commit message, or to fix or reword one, from a diff or a description of a change. Do not use for changelog entries, pull request descriptions or release notes.
---

# Commit message

Write a commit message from the staged diff or the change described.

1. Read the whole diff. Decide the single reason for the change; if there are two unrelated reasons, say the commit should be split.
2. Subject line: imperative mood ("Fix", "Add", "Remove"), at most 50 characters, no full stop at the end, capitalised first word.
3. Leave one blank line after the subject.
4. Body: explain why the change was needed and what it does differently, wrapped at 72 characters. Do not repeat the diff line by line.
5. Mention side effects, breaking changes or follow-up work in the body when they exist.

Rules
- No ticket numbers unless the user gave one; then put it on the last line as `Refs: ...`.
- Never claim the change was tested unless the user said so.
- If the diff is trivial (typo, rename), the subject alone is enough.

Output only the message in a code block.
