---
name: git-branch-name
description: Use when the user asks for a git branch name from a ticket title or issue, or says "name a branch for this ticket". Gives a lower-case hyphenated name with a type prefix like feature/ or fix/. Not for commit messages or PR titles.
---

# Git branch name

Turn a ticket title (and ticket ID if given) into one branch name.

## Steps

1. Pick the type prefix from the title:
   - `fix/` bug, error, crash, regression, broken behavior
   - `feature/` new capability or enhancement (default when unclear)
   - `chore/` maintenance, dependency bumps, config, cleanup
   - `docs/` documentation only
   - `refactor/` restructuring without behavior change
   - `test/` adding or fixing tests only
   - `hotfix/` only if the user says urgent production fix
2. Build the slug from the title:
   - lower-case everything
   - replace spaces, underscores and any run of non-alphanumeric characters with a single `-`
   - drop filler words (a, an, the, to, of, for) when that keeps the meaning
   - strip leading/trailing hyphens
   - keep it to about 5 words and at most 50 characters in the slug; cut at a word boundary
3. If a ticket ID exists (e.g. `PROJ-123`, `#456`), put it first in the slug, lower-cased: `fix/proj-123-login-crash-on-empty-password`.
4. Reply with the branch name in a code block, plus the `git switch -c <name>` command. Nothing else unless the type was a guess; then add one short line saying so.

## Rules

- Do not use upper case, spaces, underscores, dots, or non-ASCII characters (transliterate accents: é → e).
- Do not put more than one `/`, which is only after the type prefix.
- Do not include the type word twice (`fix/fix-login` → `fix/login-crash`).
- Do not ask questions; choose the best prefix and go.
- Do not create the branch or run git unless asked.

## Example

Title: "Login page crashes when password is empty" (PROJ-123)

```
fix/proj-123-login-page-crashes-empty-password
```
