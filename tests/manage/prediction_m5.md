
## M5. Documented behaviours of skills in a project (written 2026-10-09, before the run)

Source of the claims: Anthropic's Claude Code documentation, the page on skills (https://code.claude.com/docs/en/skills), read on 2026-10-09. That page describes features up to Claude Code 2.1.290; the version tested here is 2.1.286, so a feature newer than that can fail for that reason alone (the clause says so where the page names a version).
Each probe is one or two calls on a tiny project, Sonnet 5.5, print mode. A probe reports what was observed; the prediction is what the documentation says should happen.

- **M5.1 `disableBundledSkills`.** A project `.claude/settings.json` with `{"disableBundledSkills": true}` removes the bundled skills from the session: the list of skills in the session start holds only the project's own skills, and the first request shrinks by 2,000 tokens or more.
- **M5.2 `skillOverrides`.** `{"skillOverrides": {"changelog-entry": "name-only"}}` removes the description of that skill from the listing: the first request is smaller than with the override `"on"` by at least 30 tokens, and the model cannot quote the description. With `"off"` the skill is not available at all.
- **M5.3 `when_to_use`.** Text in `when_to_use` is appended to the description in the listing: a skill with a short description plus 300 characters of `when_to_use` costs between 60 and 140 tokens more than the same skill without it.
- **M5.4 description omitted.** A skill without a description is listed with the first non-empty line of its content as the description: the model quotes that line.
- **M5.5 `user-invocable: false`.** Claude can still pick the skill for a matching request (called in 2 of 2 runs), and its description is in the listing (the first request is larger than the empty session by at least 30 tokens).
- **M5.6 nested skills.** A skill in `<subfolder>/.claude/skills/` is not in the list at the start of the session and is in the list after the model reads a file in that subfolder.
- **M5.7 mention of a manual-only skill.** For a skill with `disable-model-invocation: true`, a request that names the skill in plain text ("use the changelog-entry skill to ...") makes Claude call it (called in 2 of 2 runs), while the same request without the name does not (0 of 2).
- **M5.8 `model` override.** A skill with `model: haiku`, called by name, makes the model of the following turn a Haiku model (the turn's model field names haiku).
- **M5.9 `context: fork`.** A skill with `context: fork` called by name runs in a subagent: a tool call to a subagent tool (Agent or Task) appears in the session.
- **M5.10 live reload.** A skill folder that Claude creates during the session can be called in the same session: the Skill call for it succeeds.
- **M5.11 same name in parent and child.** With a skill of the same name in the project root and in a subfolder, started from the subfolder, the documentation does not say which wins; no prediction, the observation is recorded.

Limits: one call or two per probe, so a result is an observation, not a rate; the model's report of what it sees is used for several probes; one model and version; probes M5.1 to M5.4 and M5.8 to M5.10 test documented features that could differ on 2.1.286.
