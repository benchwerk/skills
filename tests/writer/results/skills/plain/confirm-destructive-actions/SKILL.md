---
name: confirm-destructive-actions
description: Use before running any destructive or hard-to-reverse action, such as deleting files or directories, force pushing, git reset --hard, dropping or truncating database tables, overwriting uncommitted work, or killing processes. Requires the user's explicit confirmation before the action runs.
---

# Confirm Destructive Actions

Before doing anything destructive or hard to undo, stop and get the user's explicit confirmation. Do not run the action first and report afterwards.

## What counts as destructive

Treat an action as destructive if it could lose data or state that can't be trivially restored:

- **Files:** `rm`, `rm -rf`, `del`, `Remove-Item -Recurse`, `rmdir`, `find -delete`, emptying or overwriting a file or directory, bulk moves or renames that overwrite existing files.
- **Git:** `push --force` / `--force-with-lease`, `reset --hard`, `clean -f`/`-fd`, `checkout .` / `restore .` that discards changes, `branch -D`, deleting remote branches or tags, `rebase`/`commit --amend` on already-pushed commits, `stash drop`/`stash clear`, `reflog expire`, `gc --prune`.
- **Databases:** `DROP TABLE/DATABASE/SCHEMA`, `TRUNCATE`, `DELETE` or `UPDATE` without a narrow `WHERE`, destructive migrations (dropping columns or tables), `flushall`/`flushdb`, deleting collections or indexes.
- **Infrastructure and system:** `terraform destroy`, deleting cloud resources, buckets or volumes, `docker system prune`, `docker volume rm`, `kubectl delete`, killing processes or services you did not start, `chmod -R`/`chown -R` on broad paths, formatting disks.
- **Other:** uninstalling packages or removing lockfiles/environments, revoking keys or tokens, sending irreversible external messages or publishing packages, anything that modifies production.

When unsure whether something is destructive, treat it as destructive and ask.

## Not destructive (no confirmation needed)

- Reading, listing, searching, diffing, `git status`/`log`/`diff`.
- Creating new files that don't overwrite anything.
- Deleting files you created yourself earlier in this same task as temporary scratch files (say so in your summary).
- Dry runs (`--dry-run`, `git clean -n`, `terraform plan`, `SELECT`).

## How to confirm

1. **Stop before running the command.** Don't batch it with other steps.
2. **Look first.** Inspect the target so your description is accurate: list the files that match a glob, run `git status` and `git log origin/<branch>..` to see what would be lost, `SELECT COUNT(*)` for the rows affected, or use a dry run.
3. **Ask plainly**, stating:
   - the exact command or operation,
   - exactly what will be affected (paths, branch, table, row count, environment),
   - what can't be recovered, and whether a backup exists,
   - a safer alternative if there is one (e.g. `--force-with-lease`, move to trash, `git stash`, a backup or `WHERE` clause).
4. **Wait for an explicit yes.** Silence, an unrelated reply, or approval of a different action is not confirmation. Approval covers only the specific action described; ask again if the scope grows, the target changes, or it's a different destructive action later.
5. **Run only what was approved**, then report what was done. If the user declines, don't retry it in another form.

## Example

> I'm about to run `git push --force origin main`. This will overwrite 3 commits on the remote `main` (abc123..def456) that aren't in your local history, and anyone who has pulled them will diverge. Safer option: `git push --force-with-lease`, or push to a new branch. Should I proceed with the force push?

## Rules

- A user's general request ("clean up the repo", "fix the migration") is not confirmation for specific destructive steps. Ask about the concrete commands.
- Never use destructive commands to work around an error (e.g. deleting `node_modules` or a lock file, `reset --hard` to get past a conflict) without asking.
- Prefer reversible options by default: move to trash/backup instead of delete, a new branch instead of force push, a transaction or backup before a database change.
- Never target production data or shared resources without the user naming that environment in the confirmation.
- Pre-authorization only counts if the user said so explicitly for that specific kind of action in this session (e.g. "you may delete the build/ directory"). Stay within its stated scope.
