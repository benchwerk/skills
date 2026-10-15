# Part 16: managing many skills. Predictions

Written section by section, each committed **before the run it describes** (the commit time is in `git log`). A section is not edited after its run; later changes are dated notes.
Setting for every test: Claude Code 2.1.286, Sonnet 5.5 (1M window), print mode, isolated config, fresh working folder per call, the skills of the suite (`skills/`) plus synthetic ones where a crowd is needed.
Verdict rule as in the main study: *holds* when every clause is met on the point estimate; intervals are reported.

## M2a. What does Claude actually see when the skill list is long? (written 2026-10-09)

Part 14B measured only how many tokens the listing takes (a plateau of about 8,400 to 8,900 added tokens from 200 skills up). It could not say what the cap does to the text.
Here the model is asked to list every skill name it can see, in the order it sees them, and to quote the description of six named skills. The crowds are the 15 suite skills plus synthetic skills (realistic descriptions of 110 to 420 characters) up to 50, 100, 200 and 400 skills in all, three runs each.

- **M2a.1.** At 50 and 100 skills the model lists at least 95% of the installed names, and the quoted descriptions match the installed text exactly in at least 80% of the six quoted skills.
- **M2a.2.** At 400 skills it still lists at least 90% of the installed names (names are kept), but the quoted descriptions are shortened: the median of quoted length divided by installed length is at most 0.7.
- **M2a.3.** The listing order is the folder order (alphabetical by name): in at least 90% of adjacent pairs in the model's list the earlier name sorts first.
- **M2a.4.** At 400 skills the longest quoted description is at least 25% shorter than the longest installed one (a common maximum exists).
- **M2a.5.** Total tokens of the first request at 400 skills are within 5% of those at 200 skills (the plateau of Part 14B, now with realistic descriptions).

Limits: the model reports from its context and can make mistakes in a long list; each count is stated with the number of runs. One model, one version.

## M2c. Where does the description cut fall? (written 2026-10-09, after M2a, before the run)

M2a showed that, in a long list, late entries show only their name. M2c maps where. Synthetic skills named `a000` to `aNNN` (so the folder order is the numeric order), all with a description of the same length; the model is asked, for every tenth skill, to quote the first 60 characters of its description or to say that none is visible.
Crowds of 100, 200, 300 and 400 skills with descriptions of 200 characters, and of 400 skills with descriptions of 100 characters. Two runs each, 10 runs.

- **M2c.1.** In each crowd the visible descriptions are a prefix of the list: every skill with a visible description comes before every skill without one (allowing one exception in 40 per run).
- **M2c.2.** The number of skills with a visible description is the same, within 10%, in the crowds of 200, 300 and 400 skills of 200 characters (it depends on the budget, not on how many skills are installed).
- **M2c.3.** For 200-character descriptions that number is between 100 and 200.
- **M2c.4.** With 100-character descriptions at 400 skills, at least 1.5 times as many skills keep their description as with 200-character descriptions.
- **M2c.5.** Skills without a visible description are still listed by name in every crowd (names 100%).

## M2d. Do manual-only skills use up the description budget? (written 2026-10-09, before the run)

400 synthetic skills of 200-character descriptions. Configuration B: the first 300 (`a000` to `a299`) are manual-only (`disable-model-invocation: true`), the last 100 (`a300` to `a399`) automatic. Configuration C (control): all 400 automatic. In both, the model quotes the start of the description of every tenth skill from `a300` on (10 skills), and says whether it can see `a000` at all. Two runs each.

- **M2d.1.** In B all 10 probed automatic skills have a visible description (as in the 100-skill crowd of M2c).
- **M2d.2.** In C none of the 10 probed skills has a visible description (the cut at about skill 70 of M2c).
- **M2d.3.** In B the model does not see `a000` (manual-only skills are not listed for the model).

## M2b. Does a skill that shows only its name still get picked? (written 2026-10-09, before the run)

A crowd of 400 skills (399 synthetic fillers of 200-character descriptions plus one real suite skill). The target skill is `changelog-entry`, `sql-migration-review` or `bash-script-safety-review`, unchanged except for its name and position: early (position 10, description visible, by M2c) or late (position 390, name only). Name style: descriptive (`a010-changelog-entry`) or opaque (`a010-w7k2`).
Four prompts per target (`m2b_prompts.json`, material inside the prompt), two runs: 3 x 4 x 2 x 2 x 2 = 96 calls, each stopped at the model's first decision.

- **M2b.1.** Early + descriptive name: the target is called in at least 75% of the runs.
- **M2b.2.** Early + opaque name: at least 60% (the description is visible and does the work).
- **M2b.3.** Late + descriptive name: at least 40%, and at least 25 points below early + descriptive (the name alone helps, less than a description).
- **M2b.4.** Late + opaque name: at most 15% (neither a description nor a meaningful name).

## M1. Skills with similar descriptions (written 2026-10-09, before the run)

Six pairs of suite skills that are close in subject (changelog entry and release notes, SQL migration review and query tuning, commit message and pull request description, accessibility audit and SEO audit, Bash safety and portability, API errors and API versioning). In a run only the two skills of one pair are installed. The first skill (A) is unchanged; the description of the second (B) is at three levels: **distinct** (rewritten to share almost no words with A), **adjacent** (the suite text) and **near** (rewritten to share most words with A, differing only in the subject).
Eight prompts per pair (`m1_pairs.json`), four that belong to A and four to B, each with its material inside; two runs. 6 pairs x 3 levels x 8 prompts x 2 = 288 calls. A prompt counts as *correct* when the skill it belongs to is called, *wrong* when the other one is called, *none* when neither is.

- **M1.1.** Distinct: correct in at least 90% of the 96 runs.
- **M1.2.** Adjacent: correct in at least 80%.
- **M1.3.** Near: correct in at most 70%, and at least 20 points below distinct.
- **M1.4.** Near: wrong in at least 10% of the runs.
- **M1.5.** Across all levels, none (neither skill called) in at most 10% of the runs (the material is in the prompt).
- **M1.6.** In the near level the wrong picks are more frequent for prompts that belong to B (whose description was rewritten) than for prompts that belong to A, or equal.

Limits: only B's description changes; the prompts are short and cleanly one-sided, which makes real confusion less likely than in a project. One model and version, six pairs.

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

### M5b. Three probes redone after faults in the first versions (written 2026-10-09, before the run)
The first run of M5 had faults in its design, found when the observations were read: M5.6 compared the lists only by the final answer, M5.7 mentioned the skill without a slash although the documentation speaks of a name written after plain text (the examples use the slash form), and in M5.10 the write into `.claude/skills` was denied by the permission mode, so the question was not tested. The first-run observations stay in `results/m5/observations.json`; the verdicts of those three clauses are "not tested". The redone versions, with the documentation's predictions:
- **M5.6b.** The session-start list of skills (read from the start event of the session) does not contain the skill in `pkg/.claude/skills/`, and the list the model gives after reading `pkg/a.txt` contains it.
- **M5.7b.** For a manual-only skill, the request "Please do this with /changelog-entry: write the changelog entry for ..." (the slash name after plain text) makes Claude call the skill in 2 of 2 runs.
- **M5.10b.** When the skill file is created in the session with a Python command run by the model (not with the Write tool), the Skill call for it succeeds in the same session.

## MCP. What do MCP tools cost in the first request, compared with skills? (written 2026-10-09, before the run)

Popular videos say skills "fix MCP's context problem". A stub MCP server (`mcp_stub.py`, standard library) offers N tools; the first 15 carry the descriptions of the 15 suite skills and each has a small input schema. First-request size for: the empty session, 5, 15 and 40 MCP tools, and the 15 suite skills (+1,165 in the canary). Sonnet 5.5, 2.1.286, a warm-up call, each measurement twice.

- **MCP.1.** The 15 MCP tools add at least 1.3 times as many tokens as the 15 skills (at least 1,515).
- **MCP.2.** Cost grows with the number of tools without a plateau: 40 tools add at least 2.2 times what 15 add.
- **MCP.3.** The MCP tools are all present in the session's tool list at the start (not deferred): 5, 15 and 40.

Limits: one stub server, plain tool schemas; Claude Code may defer MCP tools above a threshold that this size does not reach; one model and version.

## M4. A hub skill against a flat list (written 2026-10-09, before the run)

The 15 suite skills as a flat list of automatic skills (**flat**), against one automatic skill `dev-workflows` whose description names the 15 tasks and whose body has one line per task, "Read .claude/library/<name>/SKILL.md and follow it", with the 15 skills stored as plain folders in `.claude/library/` (**hub**). A third configuration, the hub plus the 15 skills as manual-only skills (**hubmanual**), tests whether a hub can call manual-only skills.
Prompts: the 12 prompts of M2b (three targets, four prompts each, material inside), two runs per configuration, run to the end (up to 8 turns): 48 runs. Plus four unrelated developer questions (two runs per configuration, stopped at the first decision) for false calls: 16 calls. Plus 4 runs of hubmanual. About 68 calls.
Success: flat = the target skill is called; hub = `dev-workflows` is called and the file `library/<target>/SKILL.md` is read; hubmanual = the target skill is called.

- **M4.1.** Idle cost: the hub adds at most 25% of what the flat list adds (first request over the empty session; flat adds 1,165).
- **M4.2.** Success: hub in at least 75% of the 24 runs; flat in at least 90%.
- **M4.3.** Cost of a run: total input tokens over the whole run are at least 1.2 times higher in the hub than in the flat list (one more step to read the file).
- **M4.4.** False calls on the unrelated questions: hub at most 2 of 8, flat at most 1 of 8.
- **M4.5.** In hubmanual no run succeeds: Claude Code blocks calls to manual-only skills (0 of 4).

Limits: one hub design, one set of 15 skills, three targets, two runs per prompt; a bigger collection or a differently written hub may behave otherwise. One model and version.
