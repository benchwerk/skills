---
name: sql-migration-review
description: Use when the user asks to review, check or assess a SQL schema migration (up or down) for production safety. Do not use for tuning slow queries, designing schemas from scratch or writing new SELECT statements.
---

# SQL migration review

Review the migration as if it will run on a large production table.

1. Identify the database engine (default PostgreSQL if unstated) and the size of each table touched; ask only if the answer changes the verdict.
2. Check each statement for:
   - locks: `ALTER TABLE` that rewrites the table or holds an exclusive lock, adding a column with a volatile default, adding a foreign key or check constraint without `NOT VALID`
   - indexes created without `CONCURRENTLY` (PostgreSQL) or without online options
   - `NOT NULL` added to an existing column without a backfill plan
   - dropped or renamed columns and tables that running code may still use
   - data loss, type narrowing, truncation
   - a missing or untested down migration
3. Order the findings by severity: Blocker, Risk, Note.
4. For each finding give the statement, why it is a problem and a safer rewrite.

Rules
- Do not approve a migration you have not read in full.
- Say what you assumed about table sizes and engine.
- End with a one-line verdict: safe, safe with changes, or do not run.
