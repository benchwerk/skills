---
name: confirm-destructive-actions
description: Before running any destructive or hard-to-reverse action, stop and ask the user for explicit confirmation. Use whenever a step would delete files or directories (rm, rmdir, Remove-Item, del), force push or rewrite git history (push --force, reset --hard, clean -fd, branch -D, rebase on shared branches), drop or truncate database tables or delete rows without a safe WHERE, overwrite uncommitted work, kill processes, or tear down cloud/infra resources.
---

# Confirm Destructive Actions

Never run a destructive action on your own initiative. Pause, describe what will happen, and wait for an explicit "yes" from the user.

## What counts as destructive

Treat an action as destructive if it is hard or impossible to undo, or it affects data or systems beyond what the user clearly asked you to touch.

- **Files:** `rm`, `rm -rf`, `rmdir`, `del`, `Remove-Item -Recurse`, `find ... -delete`, overwriting an existing file you have not read, emptying directories, deleting build output that is not clearly regenerable.
- **Git:** `push --force` / `--force-with-lease`, `reset --hard`, `clean -f/-fd/-fx`, `checkout -- .` / `restore .` discarding changes, `branch -D`, deleting remote branches or tags, `rebase`/`commit --amend`/`filter-branch` on commits that were already pushed, `stash drop/clear`.
- **Databases:** `DROP TABLE/DATABASE/SCHEMA`, `TRUNCATE`, `DELETE` or `UPDATE` without a narrow `WHERE`, destructive migrations (dropping columns or tables), anything run against a non-local or production database.
- **Infrastructure and services:** `terraform destroy`, deleting cloud resources, buckets, volumes, containers or images with data, `kubectl delete`, `docker system prune`, revoking keys, `kill -9` on processes you did not start.
- **Other:** uninstalling packages system-wide, modifying or deleting config in the user's home directory, anything that sends irreversible messages or publishes externally.

Routine, easily reversed edits inside the task's scope (editing a tracked file, deleting a temp file you just created) do not need confirmation.

## Procedure

1. **Stop before executing.** Do not run the command, even "to see what happens".
2. **Investigate read-only first.** Look at the target so your warning is accurate: `ls`, `git status`, `git diff`, `git log origin/branch..`, `SELECT COUNT(*)`, a dry run (`--dry-run`, `-n`, `-WhatIf`, `terraform plan`).
3. **Ask for confirmation** with a short message containing:
   - the exact command or action;
   - what exactly will be lost or changed (paths, row counts, commits, branch names);
   - whether it is reversible, and how (backup, reflog, none);
   - a safer alternative if one exists (e.g. `--force-with-lease`, moving to trash, `git stash`, a backup copy, a narrower `WHERE`).
4. **Wait.** Proceed only after an explicit affirmative reply to this specific action. Silence, vague replies, or a request to "continue" are not confirmation.
5. **Execute exactly what was approved**, nothing broader. If the scope grows (more files, different branch), ask again.
6. **Report** what was done and, if relevant, how to recover.

## Rules

- Approval for one action does not carry over to later ones, even similar ones. A general instruction like "clean up" is not approval for a specific deletion; list what you plan to remove and ask.
- Prefer reversible options by default: dry run first, back up or move instead of delete, `--force-with-lease` instead of `--force`.
- Never use `--force`, `--no-verify`, `-y`, or similar flags to bypass a safety prompt without approval.
- Never force push to `main`/`master`/release branches; warn strongly even if the user asks, and confirm again.
- If the user has said explicitly (in this conversation or in CLAUDE.md) that a specific class of action is pre-approved, you may proceed for that class only, and still mention what you did.
- If you cannot ask (non-interactive run), do not perform the action; report it as skipped and explain why.

## Example confirmation

> I'm about to run `git push --force origin feature/login`. This will overwrite 3 commits on the remote branch that are not in your local history (a1b2c3, d4e5f6, 789abc). They can only be recovered if someone still has them locally. A safer option is `git push --force-with-lease`, which fails if the remote has changed unexpectedly. Do you want me to proceed with the force push, use `--force-with-lease`, or cancel?
