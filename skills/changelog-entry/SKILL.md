---
name: changelog-entry
description: Use when the user asks to write, format or fix a changelog entry or a CHANGELOG.md section for a code change or a version. Do not use for commit messages, pull request descriptions or user-facing release announcements.
---

# Changelog entry

Write an entry in the Keep a Changelog format.

1. Read the change (diff, commit list or the user's summary). If the version or date is missing, use `Unreleased`.
2. Group the items under only these headings, in this order, and omit empty ones: Added, Changed, Deprecated, Removed, Fixed, Security.
3. Write one line per item, in the present tense, starting with the thing that changed ("Retry failed uploads up to three times").
4. Describe the effect for a user of the code, not the implementation. Leave out ticket numbers, author names and file names.
5. Put breaking changes first inside their group and start the line with `**Breaking:**`.

Heading format: `## [1.4.0] - 2026-10-08` (or `## [Unreleased]`).

Rules
- One line per item; do not wrap items over several lines.
- No marketing words ("amazing", "huge").
- If an item fits two groups, choose the one a user would look in first.
- If the change is purely internal (tests, CI, formatting), say there is nothing to add instead of inventing an entry.

Output only the changelog section, ready to paste.
