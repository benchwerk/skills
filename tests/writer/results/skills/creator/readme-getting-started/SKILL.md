---
name: readme-getting-started
description: Write or update the "Getting started" section of a README.md from a project's package.json or pyproject.toml. Use when the user asks for a README quick start, install/setup/usage instructions, or a "Getting started" section for a Node/JavaScript/TypeScript or Python project.
---

# README "Getting started" writer

Generate an accurate "Getting started" section by reading the project's manifest, not by guessing. Every command written must be backed by something in the repo.

## 1. Locate and read the manifest

1. Look in the project root (or the directory the user names) for `package.json` and/or `pyproject.toml`. Also check for `README.md`, lockfiles, `.nvmrc`, `.python-version`, `Makefile`, `Dockerfile`, `.env.example`.
2. If both manifests exist, treat the one that defines the main project as primary (e.g. Python backend with a JS tooling `package.json`) and mention the other only if it has user-facing scripts. If neither exists, say so and stop; do not invent a section.
3. In a monorepo (`workspaces`, `[tool.uv.workspace]`, etc.), write the section for the root, and note how to run per-package commands.

## 2. Extract facts

**package.json**
- `name`, `description`, `private`, `bin`, `main`/`exports`/`module` (library vs CLI vs app)
- `engines.node`, `packageManager`
- `scripts`: pick out `dev`/`start`, `build`, `test`, `lint`; ignore pre/post hooks and internal scripts
- `dependencies`/`peerDependencies` (framework detection: next, vite, express, react, etc.)

**Package manager**: `packageManager` field, else lockfile (`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb`/`bun.lock` → bun, `package-lock.json` → npm). Default to npm.

**pyproject.toml**
- `[project]`: `name`, `description`, `requires-python`, `dependencies`, `optional-dependencies`, `scripts` (CLI entry points)
- `[build-system]`, `[tool.poetry]`, `[tool.uv]`, `[tool.hatch]`, `[tool.pdm]`, `[dependency-groups]`, `[tool.pytest...]`, `[tool.poe.tasks]`

**Python tool**: `[tool.poetry]` or `poetry.lock` → Poetry (`poetry install`, `poetry run`); `uv.lock`/`[tool.uv]` → uv (`uv sync`, `uv run`); `pdm.lock` → PDM; otherwise pip with a venv (`python -m venv .venv`, `pip install -e .`, add extras like `".[dev]"` when a dev/test extra exists).

## 3. Decide the audience

- **Library published to a registry** (no `private: true`, has `main`/`exports`; or a built Python package): lead with installing it as a dependency, then a minimal usage snippet, then a "Development" subsection for cloning and contributing.
- **CLI** (`bin` / `[project.scripts]`): install (global or `npx`/`uvx`/`pipx` form) and a sample invocation.
- **Application / private project**: clone, install, configure, run.

If ambiguous, include install-as-dependency only when the package is plausibly published; otherwise use the clone-and-run flow.

## 4. Write the section

Use this structure, dropping any part that has no evidence:

```markdown
## Getting started

### Prerequisites
- Node.js >= 20 (from engines) / Python >= 3.11 (from requires-python)
- <package manager if not npm/pip>

### Installation
```bash
git clone <repo url if known from repository field, else placeholder>
cd <name>
<install command>
```

### Configuration
Only if `.env.example` or similar exists: `cp .env.example .env` and name the variables that need values.

### Usage / Running
```bash
<dev or start command>
```

### Testing
```bash
<test command>
```

### Building
Only if a build script exists.
```

Rules:
- Use the real script names: `npm run dev`, `pnpm test`, `uv run pytest`. Use `npm start`/`npm test` shorthand only where valid.
- Prerequisite versions come only from `engines`, `requires-python`, `.nvmrc`, `.python-version`. Never assume a version.
- Take the repo URL from `repository` / `[project.urls]`; if absent, use `<repo-url>` and tell the user.
- Put a CLI/library usage example only if you can derive it (a `bin` name, an entry point, or an existing example in the README or `examples/`). Otherwise leave a clearly marked `<!-- TODO: add usage example -->`.
- Keep it short: a reader should be running the project in under a minute of reading. No marketing text, no restating the description beyond one line if useful.
- Match the existing README's heading level, tone, and code-fence style.

## 5. Place the output

- If `README.md` exists and has a "Getting started" (or similar: Quick start, Installation) heading, replace just that section, keeping everything else intact.
- If `README.md` exists without one, insert the section after the title/intro and badges, before detailed docs.
- If no README exists, create `README.md` with a title, the one-line description, and the section.
- If the user only asked to see the section, print it instead of editing.

## 6. Report

After writing, briefly list: which manifest and package manager were used, any placeholders or TODOs left, and any scripts you could not verify (e.g. a `test` script that is the default `echo "Error: no test specified"` should be omitted, not documented).
