---
name: traceback-explainer
description: Use when the user pastes a Python traceback or error ("what does this error mean?", "why am I getting KeyError?") and wants it explained plainly with a likely fix. Do not use for non-Python errors or writing new code.
---

# Traceback explainer

1. Read the traceback bottom-up. The last line is the exception type and message; the frames above show the call path.
2. Find the frame that matters: the last frame in the user's own code (not site-packages or stdlib). Note file, line number and the code on that line.
3. If the traceback is chained ("During handling of the above exception..." / "The above exception was the direct cause"), explain the first exception as the root cause and the later one as the consequence.
4. If the file is in the project, read the failing line and a few lines around it before guessing.
5. Pick the single most likely cause, using the exception type and message plus the code. Common ones: `KeyError` (missing dict key), `AttributeError: 'NoneType'` (a function returned None), `TypeError` (wrong argument count or type), `ImportError`/`ModuleNotFoundError` (package not installed or wrong environment), `IndexError`, `ValueError`, `FileNotFoundError` (wrong path or working directory).
6. Suggest a concrete fix as a short code change or command. Mention one alternative cause only if the evidence is truly ambiguous.

## Rules

- Do not paraphrase the traceback line by line.
- Do not explain Python basics the user did not ask about.
- Do not edit files unless the user asks you to apply the fix.
- Do not claim certainty when the traceback lacks the code; say what you would check.
- Do not list more than one alternative.

## Output

**What happened:** one or two plain sentences.
**Where:** `file:line`, and what that line was doing.
**Most likely cause:** one sentence.
**Fix:** code or command, in a block.
