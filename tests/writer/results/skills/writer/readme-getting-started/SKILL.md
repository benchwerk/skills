---
name: readme-getting-started
description: Use when the user asks to write, draft or update the "Getting started" / install / quick start section of a README for a project with a package.json or pyproject.toml. Do not use for full READMEs, API docs or changelogs.
---

# README getting-started section

1. Find the manifest in the project root: `package.json`, `pyproject.toml`, or both. Read it. Also check for lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`, `uv.lock`, `poetry.lock`, `Pipfile`) and an existing README.
2. Pick the tooling from evidence, not habit:
   - Node: lockfile or `packageManager` field decides npm/yarn/pnpm/bun; default npm.
   - Python: `[tool.poetry]` -> poetry; `uv.lock` or `[tool.uv]` -> uv; otherwise pip with a venv.
3. Collect facts:
   - Runtime requirement: `engines.node`, `requires-python` / `python`.
   - Whether it is a library or an app: `bin`, `main`/`exports`, `[project.scripts]`, a `start`/`dev` script, or a web framework dependency.
   - Scripts that matter: `dev`, `start`, `build`, `test`, `lint` (Node `scripts`; Python `[project.scripts]`, pytest/tox/nox config).
   - Optional dependency groups or extras (`[project.optional-dependencies]`, dependency groups, `peerDependencies`).
   - Env files: `.env.example` present means a copy-and-edit step.
4. Write the section with these parts, skipping any with no evidence:
   - **Prerequisites**: runtime and version.
   - **Installation**: for a published library, the install command using its real package `name`; for an app, clone, `cd`, install dependencies.
   - **Usage / Run**: the command that starts it or a minimal import example for a library; for a CLI, the `bin` name.
   - **Test** (and build if relevant): the exact script commands.
5. If a README exists with a getting-started heading, replace only that section and keep its heading level. Otherwise output the section as Markdown for the user to paste, or insert it after the intro if asked.

## Rules

- Do not invent commands, scripts, versions, URLs or package names; every command must trace to the manifest or a file you saw.
- Do not write a repository URL you did not find; use `<repo-url>` only if `repository`/`urls` is missing and a clone step is needed.
- Do not mix package managers in one section.
- Do not list every script; only the ones a newcomer needs.
- Keep it short: no badges, marketing text or contributing guidelines.
- If neither manifest exists, say so and stop.

## Output

A Markdown `## Getting started` section with fenced `bash` blocks, followed by one line naming any assumption made (for example "assumed npm; no lockfile found").
