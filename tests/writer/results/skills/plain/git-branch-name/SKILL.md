---
name: git-branch-name
description: Turn a ticket title (optionally with a ticket ID) into a git branch name, lower-case and hyphenated, with a type prefix such as feature/ or fix/. Use when the user asks for a branch name, wants to start work on a ticket, or pastes an issue/ticket title.
---

# Git branch name from a ticket title

Convert a ticket title into one branch name in the form `<type>/<slug>`, or `<type>/<ticket-id>-<slug>` when an ID is given.

## Steps

1. **Pick the type prefix** from the title's intent:
   - `feature/`: new functionality ("Add", "Support", "Implement", "Allow")
   - `fix/`: bug fixes ("Fix", "Resolve", "Crash", "Error", "Broken")
   - `hotfix/`: urgent production fixes, only if the ticket says so
   - `refactor/`: restructuring without behavior change ("Refactor", "Clean up", "Simplify")
   - `docs/`: documentation only
   - `test/`: adding or fixing tests only
   - `chore/`: tooling, dependencies, CI, config, upgrades
   - `perf/`: performance improvements
   If the user names a type, use theirs. If unclear, default to `feature/`.

2. **Build the slug** from the title:
   - Lower-case everything.
   - Drop a leading verb that duplicates the type (e.g. "Fix login crash" under `fix/` gives `login-crash`). Keep it if removing it makes the slug unclear.
   - Replace spaces, underscores, and punctuation with single hyphens.
   - Remove characters other than `a-z`, `0-9`, and `-`. Transliterate accents (é gives e).
   - Remove filler words (a, an, the, to, of, for, when, on) if the slug is too long.
   - Collapse repeated hyphens and trim hyphens from both ends.
   - Keep the slug to about 3 to 6 words and at most 50 characters, cutting at a word boundary.

3. **Add the ticket ID** if one is provided (e.g. `PROJ-123`, `#456`): lower-case it and put it first in the slug: `fix/proj-123-login-crash`. Never invent an ID.

4. **Output** the branch name in a code block, plus the command `git switch -c <branch-name>`. Do not run it unless asked. If given several titles, return one per line.

## Examples

| Ticket | Branch |
|---|---|
| Add dark mode toggle to settings page | `feature/dark-mode-toggle-settings-page` |
| Fix: crash when uploading empty file | `fix/crash-uploading-empty-file` |
| PROJ-482 Login button unresponsive on Safari | `fix/proj-482-login-button-unresponsive-safari` |
| Upgrade webpack to v5 | `chore/upgrade-webpack-v5` |
| Refactor payment service (cleanup!) | `refactor/payment-service-cleanup` |
