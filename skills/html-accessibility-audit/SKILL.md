---
name: html-accessibility-audit
description: Use when the user asks to audit, review or fix the accessibility of an HTML page, form or component: alt text, headings, labels, contrast, keyboard use, ARIA. Do not use for visual redesign, responsive layout or search engine optimisation.
---

# HTML accessibility audit

Audit the markup against the main WCAG failures.

1. Read the full HTML (and the CSS if colours or focus styles matter).
2. Check, and list each failure with the element, the problem and the fix:
   - images without `alt` (or decorative images with a non-empty one)
   - heading levels that skip, or more than one `h1`
   - form controls without a label, placeholder used as a label
   - links and buttons without a text name; "click here" links
   - colour contrast below 4.5:1 for body text (3:1 for large text), when colours are visible in the code
   - elements that cannot be reached or used with the keyboard; `tabindex` greater than 0; missing visible focus
   - ARIA that duplicates native meaning or contradicts it; `role` on the wrong element
   - missing `lang` on `html`; missing page `title`
3. Order the findings by how many users they block.

Rules
- Do not invent contrast values; compute them only from colours in the code.
- Give the corrected snippet for each finding.
- End with what could not be checked from the markup alone (screen reader behaviour, real contrast).
