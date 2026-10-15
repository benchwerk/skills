---
name: traceback-explainer
description: Use when the user pastes a Python traceback or error, or asks "what does this error mean" or "why is my script crashing". Explains it in plain English and suggests the likely fix. Not for non-Python errors.
---

# Traceback explainer

1. Find the final line of the traceback (`ExceptionType: message`). That is what went wrong. If the traceback has "During handling of the above exception" or "direct cause" chains, the last exception is the one raised, but the first is usually the root cause: name both.
2. Find the frame to blame: the deepest frame in the user's own code (skip `site-packages`, stdlib and `<frozen ...>` frames). Note its file, line and code.
3. If the file is in the project, Read that line and a few around it. Do not guess at code you can read.
4. Work out the most likely cause from the exception type, message and that line. Common ones:
   - `KeyError`/`IndexError`/`AttributeError: 'NoneType'`: a missing key, a short list, or a function that returned `None`; say where the value came from.
   - `TypeError`/`ValueError`: wrong type, wrong argument count, or bad value; say what was passed versus expected.
   - `ModuleNotFoundError`/`ImportError`: package not installed in this environment, wrong interpreter or virtualenv, circular import, or a local file shadowing a module name.
   - `FileNotFoundError`/`PermissionError`: wrong working directory or relative path, or no access.
   - `RecursionError`, `UnboundLocalError`, `IndentationError`/`SyntaxError`, `ZeroDivisionError`, `UnicodeDecodeError`: explain the usual cause for each.
5. Reply in the format below. If the traceback is truncated or the cause depends on data you cannot see, say what is missing and give the one check that would settle it.

## Rules

- Do not paste the whole traceback back.
- Do not use jargon without a few words of explanation.
- Do not list more than one alternative cause unless the evidence is truly split; lead with the most likely one.
- Do not edit files unless the user asks for the fix to be applied.
- Do not claim certainty you do not have; say "most likely" when it is a guess.

## Output format

**What happened:** one or two plain sentences.
**Where:** `file:line` and the code on it.
**Why:** the most likely cause.
**Fix:** a concrete change, as a short code snippet when it is code.
**If that is not it:** one alternative or one thing to check (omit when certain).
