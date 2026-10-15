---
name: api-error-check
description: Use when the user asks to review or fix how a REST or HTTP API handler reports errors: status codes, error bodies, validation failures, leaked internals. Do not use for writing new endpoints, authentication, API documentation or versioning.
---

# API error check

Check that failures are reported correctly and safely.

1. Read the handler and every path that can fail: bad input, missing resource, conflict, auth failure, upstream failure, unexpected exception.
2. For each path check the status code: 400 or 422 for invalid input, 401 for missing credentials, 403 for forbidden, 404 for not found, 409 for conflict, 5xx only for faults on the server side. A client mistake must never return 500.
3. Check the body: JSON with a stable `code` and a human `message`; the same shape for every error.
4. Check for leaks: stack traces, SQL, file paths, internal hostnames, secrets in messages or logs.
5. Check that unexpected exceptions are caught at one place and mapped to a generic 500.

Rules
- List findings with the line, the problem and the corrected code.
- Do not change success responses.
- Say which paths you could not see.
