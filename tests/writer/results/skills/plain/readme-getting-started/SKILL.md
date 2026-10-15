---
name: readme-getting-started
description: Write or update the "Getting started" section of a README.md from a project's package.json or pyproject.toml. Use when the user asks for a README quick start, install/usage instructions, or "getting started" docs for a Node.js or Python project.
---

# README "Getting started" writer

Generate an accurate, minimal "Getting started" section derived from the project's manifest, never from guesses.

## 1. Detect the project

Look in the project root (or the directory the user names) for:

- `package.json` → Node project
- `pyproject.toml` → Python project
- Both present → treat as a polyglot project; write a subsection for each, or ask which is primary only if the user's request is ambiguous. Do not stop to ask otherwise.
- Neither → tell the user no supported manifest was found and stop. Don't invent one.

Also check, to pick the right commands:

- Node lockfiles: `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb`/`bun.lock` → bun, `package-lock.json` or none → npm.
- Python tooling: `uv.lock` → uv; `poetry.lock` or `[tool.poetry]` → Poetry; `pdm.lock` → PDM; `[tool.hatch]` → Hatch; otherwise pip.
- `.nvmrc`, `.node-version`, `.python-version`, `.tool-versions` for runtime versions.
- Existing `README.md` (read it first; preserve its tone, heading level, and all other sections).
- `.env.example`, `docker-compose.yml`, `Makefile` for setup steps that the manifest alone does not reveal.

## 2. Extract facts

**package.json**: `name`, `description`, `engines.node`, `packageManager`, `bin`, `main`/`exports`, `private`, `scripts` (especially `dev`, `start`, `build`, `test`, `lint`), and whether it's a library (publishable, has `main`/`exports`) or an app (has `start`/`dev`).

**pyproject.toml**: `[project]` `name`, `description`, `requires-python`, `dependencies`, `optional-dependencies` (extras), `[project.scripts]` (CLI entry points), `[dependency-groups]` / `[tool.poetry.group.*]` dev groups, build backend in `[build-system]`, and test config (`[tool.pytest.ini_options]`).

Only document scripts and entry points that actually exist. Never invent a script name.

## 3. Write the section

Use `## Getting started` (match the heading level of the existing README). Include, in this order, skipping any part that doesn't apply:

1. **Prerequisites**: runtime and version (from `engines`, `requires-python`, or version files), plus any external services found (Docker, database).
2. **Installation**:
   - Apps/dev checkout: clone, `cd`, then install dependencies with the detected tool (`pnpm install`, `uv sync`, `poetry install`, `pip install -e ".[dev]"` etc.).
   - Libraries/CLIs: the package install command using the real `name` (`npm install <name>`, `pip install <name>`). Only show this if the package appears intended for publishing (not `"private": true`).
3. **Configuration**: if `.env.example` exists, show `cp .env.example .env` and mention the variables that must be set.
4. **Running**: the real dev/start command (`npm run dev`, `uv run <script>`, the `bin`/`[project.scripts]` command with an example invocation).
5. **Tests and build**: only if `test`/`build` scripts or pytest config exist.

Rules:

- Use fenced code blocks with `bash` language tags; one command per logical step.
- Use the repo's package manager consistently. Don't mix npm and yarn.
- Use the right run form: `npm run <script>` (but `npm start`/`npm test` shortcuts), `yarn <script>`, `pnpm <script>`.
- Keep it short: a newcomer should get from clone to running in under ~15 lines of commands. No marketing prose, no badges, no full API docs.
- Don't claim things you can't verify (ports, URLs, output). If a dev server port isn't in config or scripts, don't state one.
- If something is unknown but important (e.g. no `start` script and no entry point), leave it out rather than fabricating, and mention the gap to the user afterward.

## 4. Place it

- If `README.md` exists with a Getting started / Installation / Quick start section, replace just that section's body. Leave all other content untouched.
- If `README.md` exists without one, insert the section after the title/intro (before Usage/API/Contributing sections).
- If no README exists, create `README.md` with a title (`name`), the `description` as a one-line intro, then the section.
- If the user only wants the text, print it instead of writing a file.

## 5. Report

Finish with a brief summary: which manifest and package manager you detected, where the section was written, and any gaps (missing scripts, unknown Python/Node version) the user may want to fill in.

## Example output (Node app, pnpm)

````markdown
## Getting started

### Prerequisites

- Node.js >= 20
- [pnpm](https://pnpm.io) 9

### Installation

```bash
git clone <repo-url>
cd my-app
pnpm install
cp .env.example .env
```

### Running

```bash
pnpm dev
```

### Tests

```bash
pnpm test
```
````
