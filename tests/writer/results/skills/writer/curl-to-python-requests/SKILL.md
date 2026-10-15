---
name: curl-to-python-requests
description: Use when the user pastes a cURL command or asks to convert curl to Python requests code. Produces an equivalent runnable requests script. Do not use for other HTTP clients (httpx, aiohttp) or non-Python targets.
---

# cURL to Python requests

1. Parse the command: URL, method, headers, body, auth, and flags. Join `\` line continuations and strip a leading `$`.
2. Map each part using the table below.
3. Write one script: `import requests`, the call, then `print(response.status_code)` and `print(response.text)`.
4. After the code, list in one or two lines any flag you dropped or could not map.

## Mapping

| curl | requests |
|---|---|
| `-X`, `--request` | `requests.request("METHOD", url, ...)`, or `requests.get/post/...` |
| `-H`, `--header` | `headers={...}`; `Cookie:` header goes to `cookies=` only if simple, else keep it in headers |
| `-d`, `--data`, `--data-raw`, `--data-binary` | `data="..."` (string kept as-is). No `-X` means POST |
| `--data-urlencode k=v` | `data={"k": "v"}` |
| `--json '{...}'` or `-d` with JSON `Content-Type` | `json={...}` as a Python dict (also set no extra Content-Type) |
| `-F k=v`, `-F k=@file` | `data={"k": "v"}`, `files={"k": open("file", "rb")}` |
| `-u user:pass` | `auth=("user", "pass")` |
| `-b`, `--cookie` | `cookies={...}` |
| `-G` with `-d` | `params={...}` on a GET |
| `-L` | default; `-L` absent means `allow_redirects=False` |
| `-k`, `--insecure` | `verify=False` |
| `--cacert f` / `--cert f` / `--key f` | `verify="f"` / `cert=("cert", "key")` |
| `-x`, `--proxy` | `proxies={"http": p, "https": p}` |
| `-m`, `--max-time` | `timeout=N` |
| `-A`, `--user-agent` | `User-Agent` header |
| `-e`, `--referer` | `Referer` header |
| `-I`, `--head` | `requests.head(...)` |
| `--compressed` | default; omit |
| `-o file` | write `response.content` to the file in `"wb"` |
| `-s`, `-v`, `-i`, `-S` | output-only; omit and mention if relevant |

## Rules

- Put query strings in `params` only if they are plain; otherwise leave the URL untouched.
- Do not invent headers or timeouts the command did not have, except add `timeout` only if `-m` was given.
- Do not hide secrets: keep tokens as given, but if one looks real, suggest reading it from an environment variable.
- Do not call `response.json()` unless the user asked for it.
- Do not run the request. Convert only.
- If a flag is unknown, keep going and name it in the notes; do not guess.
- For several curl commands, produce one snippet each, sharing a `requests.Session()` only if cookies are carried between them.

## Output

One fenced `python` block, then the short notes line (omit if nothing was dropped).
