---
name: api-versioning-check
description: Use when the user asks whether an API change is backward compatible, needs a new version, or how to deprecate an endpoint or field. Do not use for error handling, writing endpoints or generating API documentation.
---

# API versioning check

Decide whether a change breaks existing clients.

1. Compare the old and the new contract: paths, methods, parameters, request and response fields, types, enums, defaults, status codes, ordering and pagination.
2. Classify each difference: Compatible (new optional field, new endpoint), Risky (new required input, narrower accepted values, new enum value clients may not handle), Breaking (removed or renamed field, changed type or meaning, changed status code).
3. If anything is Breaking, recommend a new version or a compatible alternative (add the new field and keep the old one).
4. For deprecations give a plan: announce, warn in responses (a `Deprecation` or `Sunset` header), measure remaining use, remove.

Rules
- Judge by what existing clients can see, not by what the code did internally.
- Name the clients or versions you assumed.
- End with a verdict: compatible, compatible with care, or breaking.
