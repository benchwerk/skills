---
name: csv-cleaning-plan
description: Use when the user has a CSV or similar table and asks what is wrong with it, how to clean it, or to plan a cleanup before loading it. Do not use for converting formats, plotting, querying or statistical analysis.
---

# CSV cleaning plan

Inspect first, plan second, and never modify the original file.

1. Read the header and a sample from the top, the middle and the end. Note the row and column counts.
2. For each column report: the type it holds, the type it should hold, the share of empty values, and odd values (mixed types, placeholders such as `N/A`, `-`, `0000`).
3. Check the whole table for: duplicate rows and duplicate keys, inconsistent casing and spelling, leading or trailing spaces, mixed date formats, mixed decimal or thousands separators, encoding problems, out-of-range values.
4. Write the plan as a numbered list. Each step names the column, the problem, the exact fix and what to do with rows that cannot be fixed.
5. Order the steps so that later steps do not depend on skipped ones.

Rules
- Show counts, not impressions ("212 of 4,030 rows").
- Keep the original file unchanged; write results to a new file.
- Say which decisions need the user (for example which duplicate to keep).
