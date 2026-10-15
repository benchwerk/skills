---
name: sql-query-tuning
description: Use when the user asks why a SQL query is slow, or asks to speed up, tune or explain the plan of a SELECT or UPDATE. Do not use for reviewing schema migrations or designing a new schema.
---

# SQL query tuning

Find why the query is slow before changing it.

1. Get the query, the table definitions and indexes, row counts, and the `EXPLAIN (ANALYZE)` output if available. If there is no plan, say what to run and why.
2. Read the plan from the most expensive node outward: sequential scans on large tables, row estimates far from actual rows, sorts or hashes spilling to disk, nested loops over large sets.
3. Check the query: functions on indexed columns, leading wildcards, implicit casts, `SELECT *`, `OR` chains, missing join conditions, unneeded `DISTINCT`.
4. Propose changes in order of expected gain: a missing index (name the columns and order), a rewrite, updated statistics.
5. For each change say what the plan should look like afterwards and how to confirm it.

Rules
- Do not suggest an index without saying what it costs on writes.
- State clearly when you are guessing without a plan.
- Keep the result of the query identical unless the user agrees to change it.
