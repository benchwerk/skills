---
name: readme-getting-started
description: Use when the user asks to write or update the "Getting started", install or quick start section of a README for a project with a package.json or pyproject.toml. Do not use for full READMEs, API docs or changelogs.
---

# README getting-started section

1. Find the manifest: read `package.json` or `pyproject.toml` in the project root (if both exist, ask nothing; use the one matching the main language and mention the other). Also check for a lockfile (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `uv.lock`, `poetry.lock`) to pick the package manager.
2. Collect only facts present in the files:
   - name, description, version
   - runtime requirement (`engines.node`, `requires-python`)
   - dependencies worth noting (system tools, native modules)
   - scripts (`dev`, `start`, `build`, `test`) or `[project.scripts]` / `[tool.poetry.scripts]` entry points
   - `bin` (package.json) or console scripts: this means a CLI, so show a usage line
3. Decide the install path:
   - Published library (not `private: true`): `npm install <name>` / `pip install <name>`.
   - App or unpublished repo: clone, then install dependencies (`npm install`, `pnpm install`, `uv sync`, `poetry install`, or `pip install -e .`).
4. Write the section: prerequisites, install, run, test. Skip any step the manifest gives no evidence for.
5. If a README exists, replace only its existing "Getting started" section (same heading level); keep the rest untouched. Otherwise print the section.

## Rules

- Do not invent scripts, commands, versions or URLs. Leave out what the manifest does not show.
- Do not describe the project's features or architecture.
- Do not use `npm` when a lockfile shows pnpm or yarn.
- Do not add badges, tables of contents or license text.
- Keep it under about 30 lines, with commands in fenced code blocks.

## Output format

```markdown
## Getting started

### Prerequisites
- Node.js >= 18

### Installation
```sh
git clone <repo-url>
cd <name>
npm install
```

### Usage
```sh
npm run dev
```

### Tests
```sh
npm test
```
```
