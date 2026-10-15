---
name: release-notes-from-log
description: Use when the user gives a git log, commit list or tag range and asks for release notes or a release announcement for users. Do not use for CHANGELOG.md sections for developers, single commit messages or pull request descriptions.
---

# Release notes from a log

Turn a commit list into notes users can read.

1. Read every commit between the two tags. Skip merge commits, formatting, CI and dependency bumps unless they change behaviour.
2. Group into: Breaking changes (first), New features, Fixes, and Other if needed.
3. Rewrite each item in plain language for someone who uses the product, not the code. Say what they can now do or what no longer breaks.
4. Merge commits that belong together into one item.
5. For each breaking change add one line on what to do about it.
6. Start with a two-sentence summary of the release.

Rules
- Do not invent features that are not in the log.
- No commit hashes, author names or internal module names in the notes.
- If the log is empty or contains only chores, say so.

Output the notes in Markdown, ready to publish.
