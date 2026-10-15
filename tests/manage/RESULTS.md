# Part 16 results: managing many skills

## M2a. What does Claude see of a long skill list? (12 calls, 2026-10-09)

The 15 suite skills plus synthetic skills (descriptions of 110 to 420 characters) up to 50, 100, 200 and 400 skills, three runs each. The model was asked to list every skill name it sees and to quote the description of six skills. Raw data: `results/m2a/raw.jsonl`; the full answers are in the same folder.

| Skills installed | Names the model lists | First request (tokens) | Descriptions visible among the 6 asked (run 1) |
| --: | --: | --: | --: |
| 50 | 50 of 50 | 23,839 | 6 |
| 100 | 100 of 100 | 27,131 | 5 |
| 200 | 200 of 200 | 27,601 | 3 |
| 400 | 400 of 400 | 28,443 | 2 |

**What happened.** The model always saw every name. What disappears as the list grows is the description. At 400 skills it answered for four of the six asked: "no description visible; only the name is listed". The two it could quote in full were the first two in the listing order (`api-error-check` and `changelog-entry`, which sort before the synthetic names). The descriptions that survive are quoted in full (240 and 218 characters): the cut is a budget over the whole list, not a shortening of each description.

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| M2a.1 at 50 and 100 skills: 95%+ of names, and 80%+ of the quoted descriptions exact | names 100%; exact 5 of 12 (41.7%). Most of the misses are the marker `[cut]`, which the prompt invited and the model added to complete descriptions; within 7 characters of the installed length: 91.7%. One of six descriptions was missing at 100 skills | fails as defined |
| M2a.2 at 400: 90%+ of names, median quoted length at most 0.7 of installed | names 100%; median 0.28 | holds |
| M2a.3 listing order is the folder order (90%+ of adjacent pairs) | 96.5% | holds |
| M2a.4 at 400 the longest quoted description is 25%+ shorter than the longest installed | 240 against 240 (the budget cuts entries, not characters) | fails |
| M2a.5 tokens at 400 within 5% of tokens at 200 | +3.1% | holds |

**Why it matters for managing skills.** Claude Code keeps every skill's name but stops showing descriptions once the list is long enough, and the entries that come later in the list lose theirs first. A skill whose description cannot be seen can only be picked by its name. So, in a large collection, a skill late in the list is harder to trigger than the same skill early in the list. The next test (M2c) finds out where the cut falls and whether the length of the descriptions changes it.

Limits: three runs per size; one model and version; the model reports what it sees in its context, and the answers were checked only for the six asked skills and for the list of names. The position effect is confounded with "synthetic against real" in this test (all real suite skills sort first); M2c removes that.

## M2c. Where does the description cut fall? (10 calls, 2026-10-09)

Synthetic skills named `a000` upward, every description the same length; the model quoted the start of the description of every tenth skill, or said none was visible. Predictions written and committed before the run (`a7d8f88`, 11:24). Raw data: `results/m2c/raw.jsonl`. Both runs of each crowd gave the same pattern.

| Skills installed | Description length | Pattern, every tenth skill (V = description visible, . = name only) | Descriptions visible up to about |
| --: | --: | :-- | --: |
| 100 | 200 | `VVVVVVVVVV` | all 100 |
| 200 | 200 | `VVVVVVVVVV..........` | skill 100 |
| 300 | 200 | `VVVVVVVV......................` | skill 80 |
| 400 | 200 | `VVVVVVV.................................` | skill 70 |
| 400 | 100 | `VVVVVVVVVVVVV...........................` | skill 130 |

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| M2c.1 visible descriptions are a prefix of the list | 10 of 10 runs, no exception | holds |
| M2c.2 the number with a visible description is within 10% at 200, 300 and 400 skills (200 characters) | about 100, 80 and 70 | fails |
| M2c.3 for 200-character descriptions that number is between 100 and 200 | 100 at 200 skills; 80 and 70 at 300 and 400 | fails |
| M2c.4 with 100-character descriptions at 400 skills, 1.5x as many keep theirs | 130 against 70 (1.86x) | holds |
| M2c.5 names are still listed in every crowd | every probed name was answered, with a description or with "none" | holds |

**What it shows.**
- The list is a budget that is filled from the top. Names of all skills are listed first, descriptions fill what is left, in folder order, and the entries at the end get only their name.
- **The more skills are installed, the fewer get a description:** with 200-character descriptions about 100 at 200 skills, 80 at 300, 70 at 400. The names of the extra skills use up budget that descriptions would have used (the first request grew only from 26,984 to 28,837 tokens, so the total stays flat as predicted in Part 14B, and what changes is how it is shared).
- **Shorter descriptions buy visibility:** at 400 skills, halving the description length from 200 to 100 characters nearly doubled the number of skills with a visible description (70 to 130).
- Resolution is ten skills (every tenth was probed).

**What it means for a project with many skills.** Beyond roughly 70 to 130 skills, some skills have no description in Claude's list and can only be picked by their name. Keep the number of automatic skills down, keep descriptions short, and name skills so that the name alone says what they are for.

Limits: one model and version, synthetic descriptions, folder order is alphabetical on this system, two runs per cell, resolution of ten skills; whether the same budget is shared with the bundled skills and with other text was not isolated. Whether a skill with only a name is still picked when the prompt matches its name is tested in M2b below.

## M2d. Do manual-only skills use up the description budget? (4 calls, 2026-10-09)

400 synthetic skills with 200-character descriptions. Configuration B: the first 300 manual-only, the last 100 automatic. Configuration C: all 400 automatic. Predictions committed before the run (`b662bbe`, 11:26). Raw data: `results/m2d/raw.jsonl`. Two runs each, identical.

| | Probed automatic skills with a visible description (of 10) | Sees the first skill `a000` | First request (tokens) |
| :-- | --: | :-- | --: |
| B: 300 manual-only + 100 automatic | 10 | no | 27,008 |
| C: 400 automatic | 0 | yes | 28,555 |

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| M2d.1 in B all 10 probed automatic skills keep their description | 10 of 10 | holds |
| M2d.2 in C none of the 10 does | 0 of 10 | holds |
| M2d.3 in B the model does not see `a000` (manual-only skills are not listed) | NO | holds |

**What it shows.** Manual-only skills are not in Claude's list at all and take no part of the budget: with 300 of the 400 skills manual-only, the other 100 are listed with full descriptions (the same as a crowd of 100). In the all-automatic crowd the same 100 skills have names only. This is the strongest tool for managing a large collection: keep rarely used skills manual-only, and the skills that should be picked automatically keep their descriptions.
Limits: one model and version, synthetic skills, two runs, resolution of ten skills; whether the right skill is then picked is not tested here.

## M2b. Does a skill that shows only its name still get picked? (96 calls, 2026-10-09)

A crowd of 400 skills (399 synthetic fillers with 200-character descriptions plus one real suite skill). The target (`changelog-entry`, `sql-migration-review` or `bash-script-safety-review`, content unchanged) sat at position 10 (description visible, by M2c) or position 390 (name only), with a descriptive name (`a010-changelog-entry`) or an opaque one (`a010-w7k2`). Four prompts per target with the material inside, two runs each. Predictions committed before the run (`b662bbe`, 11:26). Raw data: `results/m2b/raw.jsonl`.

| Position | Name | Target called | Other skill called |
| :-- | :-- | --: | --: |
| early (description visible) | descriptive | 24 of 24 (100%) | 0 |
| early | opaque | 24 of 24 (100%) | 0 |
| late (name only) | descriptive | 24 of 24 (100%) | 0 |
| late (name only) | opaque | **0 of 24 (0%)** | 0 |

The same in each of the three targets (8 of 8, 8 of 8, 8 of 8, 0 of 8). In the 24 runs where the target was not called, the model answered in text.

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| M2b.1 early + descriptive: 75%+ | 100% | holds |
| M2b.2 early + opaque: 60%+ | 100% | holds |
| M2b.3 late + descriptive: 40%+ and 25 points below early + descriptive | 100%, no gap | fails |
| M2b.4 late + opaque: 15% or less | 0% | holds |

**What it shows.** When the description is cut off, **the name alone decides**: a skill named after what it does was called in every run even with no description visible; a skill with an opaque name was called in none. So in a large collection, name skills so that the name says what they are for.
Caveat: the prompts and the names share the key words ("changelog", "migration", "script"), which is the easy case; a name that is descriptive but uses other words than the user would is untested. One model and version, three skills, 96 calls.

## M1. Skills with similar descriptions (288 calls, 2026-10-09)

Six pairs of suite skills, each pair installed alone, the second skill's description at three levels of similarity to the first (distinct, adjacent, near-duplicate), eight prompts per pair with the material inside, two runs. Predictions committed before the run (commit `b143b50`). Raw data: `results/m1/raw.jsonl`. Pairs: changelog entry and release notes, SQL migration review and query tuning, commit message and pull request description, accessibility audit and SEO audit, Bash safety and portability, API errors and API versioning.

| Description of the second skill | Right skill called | Wrong skill called | Neither called |
| :-- | --: | --: | --: |
| distinct | 94 of 96 (97.9%) | 0 | 2 |
| adjacent (the suite text) | 94 of 96 (97.9%) | 0 | 2 |
| near-duplicate | 91 of 96 (94.8%) | 0 | 5 |

All wrong outcomes were "neither called", never "the other skill". They concentrated in the second skill's prompts (distinct 2, adjacent 2, near 5, none in the first skill's prompts) and in two pairs: accessibility audit and SEO audit (2 of 16 at every level) and API errors and versioning (3 of 16 in the near level).

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| M1.1 distinct: 90%+ correct | 97.9% | holds |
| M1.2 adjacent: 80%+ correct | 97.9% | holds |
| M1.3 near: 70% or less, and 20 points below distinct | 94.8%, 3.1 points below distinct | fails |
| M1.4 near: wrong skill in 10%+ | 0% | fails |
| M1.5 neither called in 10% or less overall | 9 of 288 (3.1%) | holds |
| M1.6 wrong picks: more for prompts of the second skill, or equal | 0 and 0 | holds (equal) |

**What it shows.** Two skills whose descriptions are almost the same words did not get mixed up in this test: Claude chose by the content of the request (a changelog, a query, a script), not by a difference in the description. When similarity hurt at all, it showed as the right skill not being called, not as the wrong one being called, and by at most 5 points.
**Limits that matter.** Only two skills were installed (a crowd of look-alikes is harder); every prompt was unambiguous and carried its material; the near-duplicate descriptions still differ in the subject word, which is what the prompt names; one model and version. A prompt that fits both skills, or a crowd with several close skills, is not covered by this result.

## M7. Version canary (2026-10-09)

`canary.py` measures five first-request sizes in a few minutes: the empty session, one skill, the 15 suite skills, the same skill manual-only, and the skill called by name. It discards a first warm-up call (the first call in a fresh working folder read 88 tokens low on both versions) and measures every configuration twice. All values repeated exactly. The working folder is fixed because the path is part of the prompt (a different folder name changes the token count). Outputs: `canary_2.1.284.json`, `canary_2.1.286.json`.

| Sonnet 5.5, 1M window | Claude Code 2.1.284 | Claude Code 2.1.286 |
| :-- | --: | --: |
| empty session | 18,931 | 19,254 |
| one skill, listing | +76 | +76 |
| the 15 suite skills, listing | +1,165 | +1,165 |
| the same skill, manual-only | +0 | +0 |
| the skill called by name, on top of its listing | +434 | +434 |

**What it shows.** Between the two versions only the empty session moved (+323 tokens here; the main study measured +277 in its own folder); the cost of skills did not. A canary run on a new version tells within minutes whether earlier measurements still hold. Absolute values depend on the working folder's path; the differences do not.
Limits: Sonnet only, one machine, two versions.

## M5. Documented behaviours of skills in a project (about 25 calls, 2026-10-09)

Claims taken from Anthropic's skills documentation (https://code.claude.com/docs/en/skills, read 2026-10-09; the page describes features up to Claude Code 2.1.290, the version tested is 2.1.286). Predictions committed before the runs (`d82a462`, and `862e253` for the three redone probes). Raw observations: `results/m5/observations.json` and `results/m5/observations_b.json`. Each probe is one or two calls, so a result is an observation, not a rate.

| Probe | What the documentation says | Observed | Verdict |
| :-- | :-- | :-- | :-- |
| M5.1 `disableBundledSkills: true` in the project settings | turns off the bundled skills | the session list falls from 18 skills to 4 (the test skill plus `design`, `doctor`, `plugin-authoring`); first request 19,338 to 17,204 (-2,134) | fails as worded ("only the project's own skills"), but the setting works: 14 of 17 bundled skills removed, -2,134 tokens |
| M5.2 `skillOverrides` | `name-only` removes the description, `off` removes the skill | `on` 19,387; `name-only` 19,323 (-64), the model: "no description, only its name appears"; `off` 19,311 and the skill is not in the session list | holds |
| M5.3 `when_to_use` | appended to the description in the listing | 307 characters add 109 tokens | holds |
| M5.4 description omitted | the first non-empty line of the content is used | the model quoted that line | holds |
| M5.5 `user-invocable: false` | hidden from the `/` menu, Claude can still use it, description in context | listing +74 tokens; picked in 2 of 2 natural requests | holds |
| M5.6b nested skills | a skill in `<subfolder>/.claude/skills/` loads on the first read of a file there | not in the session-start list (17 skills); in the list after reading `pkg/a.txt` | holds |
| M5.7b a manual-only skill named as `/name` after plain text | counts as permission for Claude to run it | not called, 0 of 2 (plain request without the name: 0 of 2) | fails |
| M5.8 `model: haiku` | overrides the model for the rest of the turn | both assistant messages of the turn came from `claude-haiku-4-5` | holds |
| M5.9 `context: fork` | runs in a forked subagent | no subagent tool call appeared; the answer was produced in the same session | fails (not observed in print mode) |
| M5.10b live reload | a new skill folder is picked up without a restart | the skill file was created by a Python command during the session (checked on disk); the Skill call answered "Unknown skill: late" | fails in print mode |
| M5.11 same name in parent and child | not stated | started in the subfolder, the model quoted the child's description | observation |

The first versions of M5.6, M5.7 and M5.10 were faulty (the lists were compared only by the final answer, the manual-only name was written without a slash, and the Write tool was denied into `.claude/skills`); they are recorded as "not tested" and redone as M5.6b, M5.7b and M5.10b.

**What it shows.**
- **Correction of an earlier statement.** An earlier note said bundled skills could not be removed without removing the project's own; that was true only of the `--disable-slash-commands` flag. The settings option `disableBundledSkills` removes 14 of the 17 and keeps the project's skills. In the earlier baseline test this is the way to save about 2,100 tokens in a normal session, no flags needed.
- **`skillOverrides: name-only` is the documented version of what the listing budget does by itself:** the description goes, the name stays. It saves about 64 tokens per skill with a 218-character description.
- **`when_to_use` costs tokens in the same range per character as the description:** 307 characters added 109 tokens (about 0.36 per character); removing a 218-character description saved 64 (about 0.29). The two together are cut at 1,536 characters.
- Three documented behaviours were not seen in print mode (a name after plain text, forking, live reload); they may work in an interactive session, which these probes cannot show.
Limits: print mode only; one model and version; one or two calls per probe.

## MCP tools against skills (about 20 calls, 2026-10-09)

A stub MCP server with N tools (`mcp_stub.py`; the first 15 carry the descriptions of the 15 suite skills; each has a two-field input schema) against the same 15 descriptions as skills. First-request size, Sonnet 5.5, Claude Code 2.1.286, warm-up and two measurements per configuration, all repeated exactly. Predictions committed before the run (`d965587`, 21:20). Raw data: `results/mcp/raw.json`.

| Configuration | First request | Added over the empty session | Per item |
| :-- | --: | --: | --: |
| empty | 19,256 | - | - |
| 5 MCP tools | 19,329 | +73 | 14.6 |
| 15 MCP tools | 19,486 | +230 | 15.3 |
| 40 MCP tools | 19,942 | +686 | 17.2 |
| the 15 suite skills | 20,421 | +1,165 | 77.7 |

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| MCP.1 15 MCP tools add 1.3x the tokens of the 15 skills | 230 against 1,165 (0.2x) | fails (the opposite) |
| MCP.2 40 tools add 2.2x what 15 add (no plateau) | 686 against 230 (3.0x) | holds |
| MCP.3 all MCP tools are in the session's tool list at the start | 5, 15 and 40 present | holds |

Exploratory, after the run: on Haiku the 40 tools add +511 (23,804 to 24,315); with the 200k Sonnet model id they add +686, the same as above.

**What it shows.** In this Claude Code version an MCP tool costs about 15 tokens in the first request (apparently its name only: the tools are in the list at the start and the cost is far too small for their schemas; whether the definitions are deferred was inferred from the cost, not checked directly), against about 78 for a skill with the same description. So the popular claim that skills fix MCP's context problem does not hold for the listing: a skill is the more expensive of the two to have installed. Both grow without a plateau up to the sizes tested for MCP; skills stop growing at the listing budget (M2c).
**What this does not show.** The cost when an MCP tool is actually used (loading its definition takes an extra step, and was not measured), whether a real server's much larger schemas change the picture, and how reliably Claude picks an MCP tool whose definition it has not yet seen. One stub server, three models, two Claude Code settings.

## `/skill-doctor`, Claude Code's own skill report (2 calls, 2026-10-09)

The documentation lists a bundled `/skill-doctor` (from v2.1.252). Run as `/skill-doctor` in print mode on two projects (`results/skill_doctor.json`); it made no model call (no tool calls, no meter reading) and printed a table of the skills in the session: source, the size of each skill's one-line listing ("context"), tokens attributed over the last 7 days, and uses.

| | `/skill-doctor` | this study |
| :-- | :-- | :-- |
| the 15 suite skills, listing cost per skill | "~60" to "~90" | 76 to 78 measured per skill |
| `deep-think` V3 listing | "~190" | audit script estimate 191 |
| unused skills | "4 skills loaded but never invoked" (from the machine's session logs) | not measured |
| the missing `scripts/check_work.py` and `lenses.md` of V3 | not mentioned | found by `skill-writer/scripts/skill_audit.py` |
| broad description, instruction in the description, opaque name, how many descriptions fit the budget | not mentioned | found by `skill-writer/scripts/skill_audit.py` |

**What it shows.** Claude Code's own report agrees with these measurements on the listing cost per skill, and adds usage over the last 7 days, which these tests do not measure. It does not check what makes a skill fail: dangling file references, a description that cannot be picked, a list too long for descriptions. The two tools complement each other.
Limits: two projects, print mode; the "uses" column counts this study's own test runs on this machine.

## M4. A hub skill against a flat list (68 calls, 2026-10-09)

The 15 suite skills as a flat list of automatic skills (flat), against one automatic skill `dev-workflows` with one line per task pointing to `.claude/library/<name>/SKILL.md`, the 15 skills stored there as plain folders (hub), and the hub plus the 15 as manual-only skills (hubmanual). The 12 prompts of M2b, two runs each, run to the end (24 per configuration), four unrelated questions (two runs each) for false calls, four hubmanual runs. Predictions committed before the run (commit `3b4282b`). Raw data: `results/m4/raw.jsonl`, `results/m4/idle.json`. (A parsing error in the script stopped the first attempt after 38 rows; it was fixed and the run resumed from the saved rows.)

| | Flat | Hub |
| :-- | --: | --: |
| Added to the first request (idle) | +1,165 | +121 |
| Right skill reached | 24 of 24 | 24 of 24 (hub called and the right library file read) |
| Total input tokens over a run (mean) | 41,511 | 61,763 (1.49x) |
| Tool calls per run (mean) | 1.0 | 2.1 |
| Output tokens per run (mean) | 1,001 | 1,195 |
| False calls on unrelated questions | 0 of 8 | 0 of 8 |

Hubmanual: the hub was called and then called the manual-only `changelog-entry` in 4 of 4 runs; Claude Code blocked every one of them, and in all four the answer says the skill can only be run by the user ("reserved for you to invoke") and that it will not reproduce the workflow by hand: 0 of 4 produced the entry.

| Clause | Result | Verdict |
| :-- | :-- | :-- |
| M4.1 the hub adds at most 25% of the flat list's idle cost | 121 against 1,165 (10.4%) | holds |
| M4.2 right skill reached: hub 75%+, flat 90%+ | 100% and 100% | holds |
| M4.3 a run costs at least 1.2x the input tokens in the hub | 1.49x | holds |
| M4.4 false calls: hub 2 of 8 or fewer, flat 1 of 8 or fewer | 0 and 0 | holds |
| M4.5 a hub cannot call manual-only skills | 0 of 4 | holds |

**What it shows.** A hub skill pointing to a library of plain files cut the idle cost by 90% (121 against 1,165 tokens for 15 skills) and reached the right skill every time, at the price of one extra step per use: about 1.5 times the input tokens of a run, and one more tool call. A hub cannot use manual-only skills: the block is real, and Claude respects it by refusing instead of working around it. The saving grows with the number of skills; for a handful of skills the flat list is simpler, and for a large collection a hub is a way to keep descriptions visible (M2c) at the cost of an extra step.
Limits: 15 skills, three targets (12 prompts), clean one-sided prompts, one hub design (a one-line summary per skill in the body), one model and version, two runs per prompt. A hub with many more entries may be picked less reliably, which this test did not reach.
