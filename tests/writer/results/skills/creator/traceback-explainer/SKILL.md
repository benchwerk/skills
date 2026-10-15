---
name: traceback-explainer
description: Explains a Python traceback or exception in plain English and suggests the most likely fix. Use when the user pastes a Python traceback or error output, asks "what does this error mean", "why is this crashing", or needs help debugging a Python exception such as KeyError, TypeError, ImportError, or AttributeError.
---

# Traceback Explainer

Turn a Python traceback into a short plain-English explanation and a concrete, most-likely fix.

## Process

1. **Find the traceback.** Use the one the user pasted. If they only mention an error, look for it in the conversation or ask them to paste the full text only if none is available; do not guess from the error name alone.
2. **Read it bottom-up.**
   - The last line is the exception type and message. This is what went wrong.
   - The frame just above it is where it was raised.
   - Walk upward to find the deepest frame in the user's own code (not `site-packages` or the standard library). That is usually where the bug is.
   - For chained exceptions ("During handling of the above exception..." or "The above exception was the direct cause..."), the first exception is the root cause; explain it first.
3. **Look at the real code.** If the referenced file exists in the working directory, Read the lines around the failing line number before diagnosing. Prefer evidence from the code over pattern-matching on the message.
4. **Pick the most likely cause.** Choose one primary hypothesis. Mention at most one or two alternatives, and only if they are plausible and distinguishable.
5. **Suggest a fix** as a small, concrete code change. Apply it only if the user asked you to fix it; otherwise show it.

## Output format

Use these sections, keeping the whole answer short:

**What happened** – 1–3 sentences in plain English, no jargon without a brief definition. Name the file and line.

**Why** – the likely cause, tied to the actual code or values involved.

**Fix** – a code snippet or specific command (e.g. `pip install ...`), shown as a before/after when editing existing code.

**If that's not it** – (optional) one or two other causes and how to tell them apart, e.g. a print or check to run.

## Common patterns

- `ModuleNotFoundError` / `ImportError`: package not installed in the active environment, wrong interpreter or venv, a typo, or a local file shadowing a module name (e.g. `random.py`). Circular imports show up as "partially initialized module".
- `AttributeError: 'NoneType' object has no attribute ...`: something returned `None` (a missing return, a failed lookup, or an in-place method like `list.sort()` whose result was assigned). Find where the value came from.
- `KeyError`: key is absent from the dict; check spelling and types, or use `.get()` if absence is valid.
- `IndexError`: index past the end, often an empty list or an off-by-one.
- `TypeError`: wrong argument count or types, calling a non-callable, `str` + `int`, or unpacking `None`. Compare the call with the function signature.
- `ValueError`: right type, bad value (e.g. `int("abc")`, unpacking the wrong number of items).
- `NameError` / `UnboundLocalError`: typo, missing import, or use before assignment or in the wrong scope.
- `FileNotFoundError`: relative path resolved against the wrong working directory; print `os.getcwd()` and the absolute path.
- `RecursionError`: missing or unreachable base case.
- `IndentationError` / `SyntaxError`: look at the reported line and the line before it (unclosed bracket or quote); check for mixed tabs and spaces.
- `UnicodeDecodeError`: wrong encoding; pass `encoding="utf-8"` (or the correct one) to `open`, or use `errors=`.
- `ZeroDivisionError`, `StopIteration`, `RuntimeError: dictionary changed size during iteration`, and `asyncio` "coroutine was never awaited": explain the specific mechanism.

## Guidelines

- Write for someone who may be new to Python. Short sentences, minimal jargon.
- Be honest about uncertainty. If the cause depends on data you cannot see, say what to inspect rather than inventing a certain answer.
- Do not dump the traceback back at the user or explain every frame; focus on the frames that matter.
- Fix the cause, not the symptom: avoid suggesting a bare `except:` or silencing the error unless that is truly appropriate.
- If the traceback is truncated or lacks the final exception line, say so and ask for the rest.
