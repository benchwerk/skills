---
name: git-branch-name
description: Use when the user asks for a branch name for a ticket, issue or task title ("what should I call the branch for ..."). Gives a lower-case hyphenated name with a type prefix like feature/ or fix/. Not for commit messages or PR titles.
---

# Git branch name

1. Take the ticket title (and ticket ID if given, e.g. `PROJ-123`).
2. Pick the type prefix from the title's meaning:
   - `fix/` bug, error, crash, regression, broken behaviour
   - `feature/` new capability or user-visible addition
   - `chore/` maintenance, dependency bumps, config, cleanup
   - `docs/` documentation only
   - `refactor/` restructuring without behaviour change
   - `test/` tests only
   - `hotfix/` only if the user says urgent production fix
   If unclear, use `feature/`.
3. Build the slug: lower-case, drop a leading verb like "add"/"implement" only if the name stays clear, remove filler words (a, the, to, for, of), replace spaces and punctuation with single hyphens, strip accents and non-ASCII, trim hyphens at both ends.
4. Keep the slug to about 5 words and at most 50 characters; cut whole words from the end.
5. If a ticket ID was given, put it first in lower-case: `fix/proj-123-login-timeout`.

## Rules

- Do not use upper case, spaces, underscores, dots or consecutive hyphens.
- Do not end with a hyphen or a slash.
- Do not invent an ID that was not given.
- Do not explain at length; give one name, plus one alternative only if the type is ambiguous.

## Output

The branch name in a code block, e.g.:

`fix/login-page-timeout`
