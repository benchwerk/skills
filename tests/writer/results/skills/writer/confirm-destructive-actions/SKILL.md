---
name: confirm-destructive-actions
description: Use when you are about to delete files, force push, reset --hard, drop or truncate tables, or run any command that destroys data or cannot be undone. Asks the user to confirm first. Not for read-only or easily reversible actions.
---

# Confirm destructive actions

Before running anything that destroys data or is hard to undo, stop and get an explicit yes from the user.

## Steps

1. Spot the action. It is destructive if it removes or overwrites data that is not safely recoverable. Examples:
   - Files: `rm -rf`, `Remove-Item -Recurse`, `del`, overwriting a file you have not read, emptying a directory.
   - Git: `push --force` / `--force-with-lease`, `reset --hard`, `clean -fd`, `checkout -- .`, `branch -D`, deleting remote branches or tags, `rebase` or `commit --amend` on pushed commits, `stash drop`.
   - Databases: `DROP TABLE/DATABASE/SCHEMA`, `TRUNCATE`, `DELETE` or `UPDATE` without a narrow `WHERE`, destructive migrations, `flushall`.
   - Infrastructure and other: `terraform destroy`, `kubectl delete`, `docker system prune`, `docker volume rm`, deleting cloud resources or buckets, revoking keys, uninstalling, killing processes that hold unsaved work.
2. Look at the target first with a read-only command (`ls`, `git status`, `git log origin/..HEAD`, `SELECT COUNT(*) ... WHERE ...`) so you know exactly what would be lost.
3. Ask before acting. State in the message:
   - the exact command;
   - what will be lost (paths, row counts, commits, branch names);
   - whether it can be undone, and how (backup, reflog, none);
   - a safer option if one exists (move to trash, `--force-with-lease`, a backup or dry run first).
4. Stop and wait for the reply. Do not run the command in the same turn as the question.
5. Run only what the user approved. If the scope grows (more paths, a different branch), ask again.

## Rules

- Earlier approval covers only that command and target, not later ones.
- A broad instruction such as "clean up" or "fix it" is not confirmation of a specific deletion.
- Do not hide a destructive step inside a script, chained command, or `&&` list. Show it.
- Prefer a dry run (`--dry-run`, `-WhatIf`, `git clean -n`) and show its output with the question.
- Do not ask for read-only commands, new files, or changes to files that git tracks and can restore. Don't pile on questions.
- Do not work around a refusal or a missing answer by another route to the same result.
- Only skip the question if the user has explicitly said to proceed without asking for that action, and say you are doing so.

## Format

> About to run: `git push --force origin main`
> Effect: overwrites 3 commits on origin/main (a1b2c3..d4e5f6); others who pulled them will diverge. Recoverable only from a local reflog.
> Safer option: `--force-with-lease` on a feature branch.
> Proceed? (yes / no)
