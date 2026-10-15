---
name: traceback-explainer
description: Explains a Python traceback or exception in plain English and suggests the most likely fix. Use when the user pastes a Python traceback or error output, asks "what does this error mean", "why is this crashing", or wants help debugging a Python exception.
---

# Traceback Explainer

Turn a Python traceback into a short, plain-English diagnosis and a concrete fix.

## Steps

1. **Get the traceback.** Use what the user pasted. If they only point to a log or a failing command, read the log or ask them to paste it. Don't run anything with side effects to reproduce it.
2. **Read it bottom-up.**
   - The last line is the exception type and message. That is what went wrong.
   - The frames above it show how the program got there. The last frame in the user's own code (not `site-packages` or the stdlib) is usually where the bug is.
   - With chained exceptions ("During handling of the above exception, another exception occurred" or "The above exception was the direct cause"), the first exception is usually the root cause. The last one is just the symptom.
3. **Look at the code.** If the traceback names files in the current project, open the referenced lines with Read, plus a little surrounding context, before guessing. Check that the file still matches the traceback.
4. **Pick the most likely cause.** Use the common patterns below, but base the answer on the actual code and values, not on the exception type alone.
5. **Answer in the format below.** If you edited nothing, say so. Only apply the fix if the user asks.

## Common patterns

| Exception | Usual cause |
|---|---|
| `AttributeError: 'NoneType' object has no attribute X` | A function returned `None` (missing `return`, failed lookup, or an in-place method like `list.sort()` whose result was assigned). |
| `TypeError: ... not subscriptable / not callable / unsupported operand` | The value is not the type the code assumes (e.g. `None`, str vs int, calling a variable that shadows a function). |
| `TypeError: f() takes N positional arguments but M were given` | Wrong argument count, or a method missing `self`. |
| `KeyError` / `IndexError` | The key or index isn't present. Check the data's real shape, and whether it is empty. |
| `ValueError` | Right type, unacceptable value (e.g. `int("abc")`, unpacking the wrong number of items). |
| `NameError` / `UnboundLocalError` | Typo, missing import or definition, or a variable assigned in only one branch or shadowed in a function. |
| `ImportError` / `ModuleNotFoundError` | Package not installed in the *active* environment, wrong name, circular import, or a local file shadowing a module name. |
| `FileNotFoundError` | Wrong path or wrong working directory. Use an absolute path or one built from `__file__`. |
| `RecursionError` | Missing or unreachable base case. |
| `UnicodeDecodeError` | Wrong encoding. Pass `encoding="utf-8"` or the file's real encoding, or open in binary mode. |
| `ZeroDivisionError` | Denominator is 0, often from empty input. |
| `json.JSONDecodeError` | Empty or non-JSON input, such as an HTTP error page or an empty file. |
| `ConnectionError` / `TimeoutError` | Network, host, port, or service availability, not a code bug. Suggest retries or timeouts if appropriate. |

## Output format

**What happened** — one or two sentences in plain English, with no jargon left unexplained.

**Where** — the file and line (`path:line`) most likely responsible, and the one-line snippet if known.

**Why** — the most likely cause, tied to the actual code or values. If you're inferring because you couldn't see the code, say so.

**Fix** — the smallest concrete change, as a short code snippet or diff.

**If that's not it** — up to two alternative causes, each with a quick way to check (a print, a debugger breakpoint, `type(x)`, `pip list`).

## Guidelines

- Be brief. Don't walk through every frame; mention only the ones that matter.
- Don't be confidently wrong. If the traceback alone is ambiguous, state your best guess and what would confirm it.
- Prefer fixing the root cause over wrapping the failure in `try/except`. Suggest catching the exception only when the failure is expected and can be handled.
- Don't suggest broad changes such as upgrading packages, rewriting modules, or switching Python versions unless the traceback points to a version or compatibility issue.
- Redact nothing yourself, but don't repeat secrets (tokens, passwords) that appear in the traceback.
