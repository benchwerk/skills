---
name: confirm-destructive-actions
description: Use when about to delete files, force push, reset --hard, drop or truncate tables, or run any command that destroys data. Asks the user to confirm first. Do not use for read-only or easily undone actions.
---

# Confirm destructive actions

1. Before running a command, check whether it destroys or overwrites data that cannot easily be restored. Examples:
   - Files: `rm -rf`, `del`, `Remove-Item -Recurse`, overwriting a file you have not read, emptying a folder.
   - Git: `push --force`, `reset --hard`, `clean -fd`, `branch -D`, `checkout -- .`, `stash drop`, rewriting published history.
   - Data: `DROP TABLE/DATABASE`, `TRUNCATE`, `DELETE` or `UPDATE` without a narrow `WHERE`, destructive migrations.
   - Infrastructure: `terraform destroy`, `kubectl delete`, `docker system prune`, deleting cloud resources or branches on a remote.
2. If it is destructive, stop. Do not run it yet.
3. Look at the target first with a read-only command (`ls`, `git status`, `git log`, `SELECT count(*)`) so you can state exactly what will be lost.
4. Ask the user to confirm, in one short message: the exact command, what it will affect (paths, row counts, branch and remote), and whether it can be undone. Offer a safer option if one exists (move to trash, `--force-with-lease`, backup or dry run first).
5. Wait for an explicit yes. Run it only after that, and only the command that was approved.

## Rules

- Do not treat an earlier approval as covering a different or wider command.
- Do not batch several destructive actions under one vague question; list each one.
- Do not ask for read-only commands, creating files, or changes that git can undo, such as editing a tracked file.
- Do not work around a refusal or a silence with another destructive route.
- Do not use wildcards or `-f` flags to skip prompts the tool would show.

## Output format

> About to run: `<command>`
> Affects: <what will be deleted or overwritten>
> Reversible: <yes/no, how>
> Safer option: <if any>
> Proceed?
