---
name: curl-to-python-requests
description: Use when the user pastes a cURL command or asks to convert, translate or rewrite curl as Python / the requests library. Outputs equivalent requests code. Do not use for httpx, aiohttp, other languages or explaining curl flags.
---

# cURL to Python requests

1. Parse the command: URL, method, headers, body, auth, other flags. Strip a leading `$`, line-continuation `\` or `^`, and shell quoting.
2. Map each part:
   - `-X METHOD` / `--request`: `requests.request("METHOD", ...)`, or `requests.get/post/...`. No `-X` but a body (`-d`, `-F`) means POST; `-G` moves `-d` data into `params`; `-I`/`--head` means HEAD.
   - `-H "K: V"`: entry in `headers={}`. Put `Cookie` headers and `-b` in `cookies=` or leave in headers.
   - `-d` / `--data` / `--data-raw` / `--data-binary`: if the body is JSON (Content-Type `application/json` or it looks like JSON), use `json={...}` and drop the Content-Type header; otherwise `data=` (dict for form-encoded, string/bytes for raw). Multiple `-d` are joined with `&`.
   - `--data-urlencode k=v`: `data={"k": "v"}`.
   - `-F k=v` / `-F k=@file`: `files=` (and `data=` for plain fields); open files with `open(path, "rb")`. Do not set Content-Type manually.
   - `-u user:pass`: `auth=("user", "pass")`. `-H "Authorization: Bearer X"` stays a header.
   - `-L`: default (redirects followed for GET); for other methods pass `allow_redirects=True`. Without `-L`, pass `allow_redirects=False`.
   - `-k` / `--insecure`: `verify=False`. `--cacert f`: `verify="f"`. `--cert c --key k`: `cert=("c", "k")`.
   - `-x` / `--proxy URL`: `proxies={"http": URL, "https": URL}`.
   - `-m` / `--max-time N`, `--connect-timeout N`: `timeout=N`.
   - `-A` / `--user-agent`: `User-Agent` header. `-e`: `Referer` header.
   - `--compressed`: nothing (requests handles gzip).
   - `-o file` / `-O`: write `response.content` to the file. `-s`, `-v`, `-i`: ignore, except mention `-i` means print `response.headers`.
   - `--http2`, `--retry`, other unsupported flags: omit and list them in a note.
3. Write a short runnable script: `import requests`, variables for url/headers/payload, one call, then `print(response.status_code)` and `print(response.text)` (use `response.json()` when JSON is expected).
4. Add `response.raise_for_status()` only if the user asks for error handling.

## Rules

- Keep header and value text exactly as given; never invent values or placeholders for secrets already shown.
- Do not run the request.
- Do not add classes, retries, sessions or logging unless asked. Use `requests.Session()` only for multiple curl commands sharing cookies.
- If a flag is ambiguous or unsupported, say so in one line below the code.

## Output

One fenced `python` block, then at most three lines of notes (dropped flags, assumptions such as JSON vs form body).
