---
name: curl-to-python-requests
description: Convert a cURL command into equivalent, runnable Python `requests` code. Use when the user pastes a `curl ...` command (or says "convert this curl", "curl to python", "translate to requests") and wants Python code that performs the same HTTP request.
---

# cURL to Python requests

Translate a cURL command into idiomatic Python using the `requests` library. The result must behave the same as the original command. Do not run the request unless the user asks.

## Process

1. Tokenize the command as a POSIX shell would. Handle quotes, `\` line continuations, `$'...'` strings, and Windows `^` continuations. Ignore a leading `curl`.
2. Map each flag using the table below.
3. Emit a short, self-contained script, then a brief list of any flags that could not be mapped exactly.

## Flag mapping

| cURL | requests |
|---|---|
| URL (positional or `--url`) | first argument to `requests.request` |
| `-X`, `--request METHOD` | `method` |
| `-H`, `--header "K: V"` | entry in `headers` dict. A `K;` header with no value means an empty value. `K:` with nothing after it means remove the header, so omit it. |
| `-d`, `--data`, `--data-ascii`, `--data-binary` | `data=` (string/bytes). Defaults the method to POST. Multiple `-d` flags are joined with `&`. |
| `--data-raw` | `data=` as a literal string, with no `@file` handling |
| `--data-urlencode k=v` | `data={"k": "v"}` (requests encodes it) |
| `-d @file` / `--data-binary @file` | `data=open("file", "rb").read()` (`-d` strips newlines, `--data-binary` does not) |
| `--json '{...}'` | `json=` with the parsed object. cURL also sets Content-Type and Accept to JSON. |
| `-d '{...}'` with a JSON Content-Type | prefer `json={...}` if the body parses as JSON. Otherwise keep `data=` and the header. |
| `-F`, `--form k=v` | `data={"k": "v"}` plus `files=` (see below), which makes the request multipart |
| `-F k=@path` | `files={"k": open("path", "rb")}`. `;type=mime` becomes a 3-tuple `(filename, fileobj, mime)`. |
| `-F k=<path` | the field value is the file contents, so use `data={"k": open(path).read()}` |
| `-u`, `--user user:pass` | `auth=("user", "pass")` |
| `--basic` | default for `auth=` |
| `--digest` | `auth=HTTPDigestAuth(user, pw)` from `requests.auth` |
| `-H "Authorization: Bearer T"` | keep as a header |
| `-b`, `--cookie "a=1; b=2"` | `cookies={"a": "1", "b": "2"}`. If the argument is a filename, mention it. |
| `-A`, `--user-agent` | `headers["User-Agent"]` |
| `-e`, `--referer` | `headers["Referer"]` |
| `-L`, `--location` | `allow_redirects=True` (the requests default for GET but not HEAD) |
| no `-L` | `allow_redirects=False`. cURL does not follow redirects by default, so add this for fidelity. |
| `--max-redirs N` | set `session.max_redirects = N` |
| `-k`, `--insecure` | `verify=False` (add a comment warning about it, and optionally `urllib3.disable_warnings()`) |
| `--cacert path` | `verify="path"` |
| `-E`, `--cert cert[:pw]` | `cert="cert"` or `cert=("cert", "key")` with `--key` |
| `-x`, `--proxy URL` | `proxies={"http": URL, "https": URL}` |
| `-m`, `--max-time S` | `timeout=S` |
| `--connect-timeout S` | `timeout=(S, read_timeout)` |
| `-I`, `--head` | `method="HEAD"` |
| `-G`, `--get` | send `-d` data as query `params=` with the GET method |
| `-o file` / `-O` | write `response.content` to the file |
| `-s`, `-S`, `-v`, `-i`, `-w` | no effect on the request. Mention `-i` and `-v` only if useful (print `response.headers`/`status_code`). |
| `--compressed` | requests already sends `Accept-Encoding` and decodes. Nothing to add. |
| `-0`, `--http1.1`, `--http2` | not supported by requests. Note it. |
| `--retry N` | mount `HTTPAdapter(max_retries=N)` on a Session |
| `--path-as-is`, `--resolve`, `--interface`, `--unix-socket` | no direct equivalent. Say so. |

Combined short flags such as `-sSLk` must be split. A flag glued to its value (`-XPOST`, `-HAccept:x`) is allowed.

## Details that are easy to get wrong

- **Method inference:** with a body (`-d`, `-F`, `--json`) and no `-X`, the method is POST. With `-I` it is HEAD. Otherwise GET.
- **Content-Type:** with `-d` and no explicit header, cURL sends `application/x-www-form-urlencoded`. requests does the same when `data` is a dict, but for a string body you must set the header explicitly to match.
- **Query strings:** leave them in the URL unless they are long or have many parameters. Then move them to `params=` and keep the encoding the same. Do not double-encode.
- **Body fidelity:** if `-d` holds form-style data (`a=1&b=2`) and no Content-Type was given, either keep the string or convert it to a dict. Use a dict only when the keys are unique and there are no special encodings.
- **JSON bodies:** write them as Python dicts (`True`/`False`/`None`, not `true`/`false`/`null`). If the JSON is invalid, or the exact bytes matter (such as signed payloads), keep the string with `data=`.
- **Multipart:** do not set a `Content-Type: multipart/form-data` header by hand, because requests must add the boundary. Drop that header.
- **Secrets:** keep the values the user provided, but if they look like real tokens, read them from `os.environ` and note that you did so. Do not invent values.
- **Duplicate headers:** a dict cannot hold repeated headers. Combine them with a comma where valid, or tell the user.
- **`Cookie` header:** it may stay in `headers`, or become `cookies=`. Either works. Prefer `cookies=` when `-b` was used.
- **Timeouts:** cURL has no default timeout, while requests waits forever by default. Add `timeout` only if the command specified one.

## Output format

Respond with a single fenced `python` block, then notes.

```python
import requests

url = "https://api.example.com/v1/items"
headers = {
    "Authorization": "Bearer TOKEN",
    "Content-Type": "application/json",
}
payload = {"name": "widget", "qty": 3}

response = requests.post(url, headers=headers, json=payload, timeout=30)
response.raise_for_status()
print(response.status_code)
print(response.json())
```

Guidelines for the code:

- Use the shorthand (`requests.get`, `.post`, etc.) when the method is standard. Use `requests.request("METHOD", ...)` otherwise.
- Use a `requests.Session()` only when cookies, retries, or max-redirects need it.
- Print `response.status_code` and `response.text` (or `.json()` if the body is clearly JSON, such as when an `Accept: application/json` header is sent).
- Add `raise_for_status()` only when the user did not use `-f/--fail`. If `-f` was used, it is required.
- Keep the code minimal and readable. No classes or helper functions.
- Add `import` lines only for what is used (`os`, `json`, `HTTPDigestAuth`).

After the code, add a "Notes" list only when something needs it: unsupported or approximated flags, security warnings (`verify=False`, credentials in the command), or assumptions you made. Skip the section when the conversion is exact.

## Example

Input:

```bash
curl -X POST https://api.example.com/login \
  -H 'Content-Type: application/json' \
  -d '{"user":"ann","pass":"s3cret"}' \
  -u admin:hunter2 -k -m 10
```

Output:

```python
import requests

response = requests.post(
    "https://api.example.com/login",
    json={"user": "ann", "pass": "s3cret"},
    auth=("admin", "hunter2"),
    verify=False,  # equivalent to curl -k; disables TLS verification
    timeout=10,
    allow_redirects=False,
)
print(response.status_code)
print(response.text)
```

Notes:
- `-k` maps to `verify=False`, which is insecure. Avoid it outside testing.
- `allow_redirects=False` matches cURL's default of not following redirects (no `-L` was given).
- The `Content-Type: application/json` header is set automatically by `json=`.
