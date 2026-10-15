---
name: git-branch-name
description: Turn a ticket title (Jira, Linear, GitHub issue, etc.) into a git branch name, lower-case with hyphens and a type prefix like feature/ or fix/. Use when the user asks for a branch name, wants to start work on a ticket, or pastes a ticket title/ID and mentions branching.
---

# Git branch name from a ticket title

Convert a ticket title (and optional ticket ID) into one branch name.

## Format

```
<type>/<ticket-id-if-any>-<slug>
```

Examples:

| Ticket title | Branch |
|---|---|
| Add dark mode toggle to settings page | `feature/add-dark-mode-toggle-to-settings-page` |
| PROJ-123: Crash on login when email has plus sign | `fix/proj-123-crash-on-login-when-email-has-plus-sign` |
| Update README with install steps | `docs/update-readme-with-install-steps` |
| Upgrade eslint to v9 | `chore/upgrade-eslint-to-v9` |

## Choosing the type prefix

Pick from the title's wording; if the user states a type, use theirs.

- `feature/` — new capability or enhancement (add, implement, support, introduce). Default when unclear.
- `fix/` — bug, crash, error, regression, broken behavior (fix, resolve, crash, fails).
- `hotfix/` — only if the ticket says urgent/hotfix/production incident.
- `docs/` — documentation only.
- `refactor/` — restructuring with no behavior change (refactor, clean up, simplify, rename).
- `chore/` — dependencies, tooling, config, CI, build (upgrade, bump, migrate).
- `test/` — adding or fixing tests only.
- `perf/` — performance improvements.

## Slug rules

1. Lower-case everything.
2. If a ticket ID (e.g. `PROJ-123`, `#456`) is present, keep it after the prefix, lower-cased (`proj-123`, `456`). Never invent one.
3. Drop a leading type word that duplicates the prefix only if the result is still clear (e.g. "Fix crash on login" → `fix/crash-on-login`). Otherwise keep the words.
4. Replace spaces, underscores, and punctuation with single hyphens; remove characters other than `a-z`, `0-9`, `-` (transliterate accents: é → e; drop emoji, quotes, backticks).
5. Collapse repeated hyphens; trim hyphens from both ends of the slug.
6. Remove filler words (a, an, the, to, of) only when needed to stay short.
7. Keep the whole branch name at most ~60 characters, cutting at a word boundary — never mid-word, and keep the ticket ID.
8. Only one `/`, after the type. No trailing `/`, `.`, or `.lock`; no `..`, spaces, `~`, `^`, `:`, `?`, `*`, `[`, `\`.

## Output

Reply with the branch name in a code block, plus the ready command:

```
git switch -c feature/add-dark-mode-toggle-to-settings-page
```

Do not ask clarifying questions; make the best choice and mention in one line which type was assumed if it was ambiguous. If given several titles, return one branch per line. Only run git commands if the user asks you to create the branch.
