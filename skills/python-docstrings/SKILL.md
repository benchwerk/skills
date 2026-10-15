---
name: python-docstrings
description: Use when the user asks to add, write or fix docstrings for Python functions, classes or modules. Do not use for type hints, unit tests, README text or refactoring.
---

# Python docstrings

Write Google-style docstrings.

1. Read the whole function (and the class it belongs to) before documenting it.
2. First line: a one-line summary in the imperative or a plain noun phrase, ending with a full stop, under 80 characters.
3. Add a blank line and a short description only if the summary is not enough.
4. `Args:` one entry per parameter: `name (type): meaning`. Skip `self` and `cls`.
5. `Returns:` what comes back and its type, unless the function returns nothing.
6. `Raises:` every exception the code raises or lets pass on purpose.
7. Keep the code unchanged. Only add or replace docstrings.

Rules
- Do not restate the code; say what it is for and what the caller must know.
- Keep existing correct docstrings; fix only wrong or missing parts.
- Do not document private helpers unless asked.

Output the complete changed code, not a fragment.
