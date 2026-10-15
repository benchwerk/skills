---
name: html-seo-audit
description: Use when the user asks to review an HTML page or site for search engine optimisation: title, meta description, headings, canonical, structured data, links. Do not use for accessibility audits, performance tuning or writing marketing copy.
---

# HTML SEO audit

Audit what a search engine reads from the page.

1. Read the full HTML head and body.
2. Check, and list each finding with the element and the fix:
   - `title`: present, unique, about 50 to 60 characters, the main topic first
   - meta description: present, about 150 characters, matches the page
   - one `h1` that matches the title's topic; sensible heading order
   - canonical link, robots meta, hreflang if the page has language versions
   - structured data present and valid JSON
   - internal links with descriptive text; images with useful `alt` and file names
   - Open Graph and social tags
3. Order the findings by expected effect on search results.

Rules
- Do not promise rankings.
- Say which checks need the live site (indexing, speed, links from other sites).
- Give the corrected tag for every finding.
