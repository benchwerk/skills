---
name: curl-to-python-requests
description: Convert a cURL command into equivalent Python code using the requests library. Use when the user pastes a curl command (or "Copy as cURL" output from browser devtools, API docs, etc.) and wants it translated to Python requests, or asks to port a curl call to Python.
---

# cURL to Python requests

Translate the given cURL command into a faithful, runnable Python `requests` snippet.

## Process

1. Parse the command: join `\` / `^` / backtick line continuations, and respect shell quoting (`'...'`, `"..."`, `$'...'`).
2. Map each flag using the table below.
3. Output one Python code block, then a short list of notes (only for flags that were approximated, dropped, or need user action).
4. Do not execute the request. Never invent credentials; keep the ones given, but if a token or password looks real, suggest moving it to an environment variable.

## Flag mapping

| curl | requests |
|---|---|
| URL | `requests.request(method, url, ...)` or `requests.get/post/...` |
| `-X`, `--request M` | method `M` |
| `-H`, `--header "K: V"` | entry in `headers={}` (an empty `K;` or `K:` removes the header; omit it) |
| `-d`, `--data`, `--data-raw`, `--data-ascii` | `data="..."`; implies POST if no `-X` |
| `--data-binary` | `data=b"..."` or `data=open(path, "rb")` for `@file` |
| `--data-urlencode k=v` | `data={"k": "v"}` (requests encodes it) |
| `-d @file` | `data=open("file", "rb")` (note: curl `-d @file` strips newlines; mention if it matters) |
| `--json '{...}'` | `json={...}` (curl also sets Content-Type and Accept to JSON) |
| body is JSON with `Content-Type: application/json` | prefer `json=<dict>` when the body parses as valid JSON; otherwise keep `data=` string |
| `-F`, `--form k=v` | `files={"k": (None, "v")}` |
| `-F k=@path` | `files={"k": open("path", "rb")}`; keep `;type=` as the third tuple item |
| `-u`, `--user u:p` | `auth=("u", "p")` |
| `--digest -u u:p` | `auth=HTTPDigestAuth("u", "p")` |
| `--oauth2-bearer T` / `-H "Authorization: Bearer T"` | header `Authorization: Bearer T` |
| `-b`, `--cookie "a=b; c=d"` | `cookies={"a": "b", "c": "d"}` (a file argument: load it and note it) |
| `-A`, `--user-agent` | `User-Agent` header |
| `-e`, `--referer` | `Referer` header |
| `-L`, `--location` | default behavior (`allow_redirects=True`) for GET; for non-GET set `allow_redirects=True` explicitly. Without `-L`, set `allow_redirects=False` |
| `-k`, `--insecure` | `verify=False` (add a warning note; optionally `urllib3.disable_warnings()`) |
| `--cacert F` | `verify="F"` |
| `--cert C` / `--key K` | `cert=("C", "K")` or `cert="C"` |
| `-x`, `--proxy URL` | `proxies={"http": URL, "https": URL}` |
| `-m`, `--max-time S` | `timeout=S` |
| `--connect-timeout S` | `timeout=(S, read_timeout)` |
| `-G`, `--get` with `-d` | send the `-d` pairs as `params={}` on a GET |
| `-I`, `--head` | `requests.head(...)` |
| `--compressed` | default (requests sends `Accept-Encoding` and decodes); no code needed |
| `-o file` / `-O` | write `response.content` to the file (`open(..., "wb")`) and use `stream=True` with `iter_content` for large downloads |
| `-s`, `-S`, `-v`, `-i`, `-w` | no equivalent needed; for `-i`/`-v` optionally print `response.status_code` and `response.headers` |
| `--http1.1`, `--http2`, `-4`, `-6` | not supported by requests; mention in notes |
| `--retry N` | mount an `HTTPAdapter(max_retries=Retry(total=N))` on a `Session` |
| `-H "Cookie: ..."` | keep as a header, or split into `cookies=` |

Unknown flags: leave them out of the code and list them in the notes rather than guessing.

## Details to get right

- Query strings in the URL may stay in the URL. If there are many parameters, moving them to `params={}` is more readable; both are fine, but do not double-encode.
- A `-d` body with no `Content-Type` header: requests sends `application/x-www-form-urlencoded` for dict/str `data`, matching curl. If the body is a JSON string and the header says JSON, use `json=`, and drop the redundant `Content-Type` header (requests sets it).
- Multiple `-d` flags are joined with `&`.
- Multiple `-H` with the same name: last wins in a dict; note it if relevant.
- With `-F`, do not set `Content-Type` manually; requests must generate the multipart boundary. Drop any such header from the dict.
- Method defaults: GET, or POST if there is any body/form. `-X` always overrides.
- Several URLs in one command: emit one request per URL.
- Browser "Copy as cURL" output includes noisy headers (`sec-ch-ua`, `sec-fetch-*`, `accept-language`). Keep them by default for fidelity, and mention that most can be removed.

## Output format

````
```python
import requests

url = "https://api.example.com/items"
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json",
}
payload = {"name": "widget"}

response = requests.post(url, headers=headers, json=payload, timeout=30)
response.raise_for_status()
print(response.status_code)
print(response.json())
```
````

Conventions:
- Use `import requests` only (plus `from requests.auth import HTTPDigestAuth` etc. when needed).
- Name variables `url`, `headers`, `params`, `data`/`json`, `cookies`, `auth`, `files`.
- Always include a `timeout` (use the curl value, else 30) and note that curl has none by default.
- Use `response.json()` when the expected response is JSON (Accept header or JSON body), otherwise `response.text`.
- Use a `requests.Session()` only for multiple requests, cookies that must persist, or retries.
- Keep the snippet minimal; no classes or helper functions unless the command has several URLs.

## Example

Input:

```
curl -X POST https://api.example.com/v1/users \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer abc123' \
  -d '{"name": "Ada", "admin": false}' -k
```

Output:

```python
import requests

url = "https://api.example.com/v1/users"
headers = {
    "Authorization": "Bearer abc123",
}
payload = {"name": "Ada", "admin": False}

response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)
print(response.status_code)
print(response.json())
```

Notes:
- `-k` became `verify=False`, which disables TLS verification; avoid it outside testing.
- `Content-Type` is set automatically by `json=`.
