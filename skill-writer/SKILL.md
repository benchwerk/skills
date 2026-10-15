---
name: skill-writer
description: Use when the user asks to create, write, rewrite, improve or review a Claude Code skill (a SKILL.md file), or asks why a skill is not being picked or is too expensive. Do not use for writing slash commands, CLAUDE.md files or general prompts.
---

# Skill writer

Write the skill so that Claude actually picks it, and cheaply. These rules come from measurements (benchwerk skills study, Claude Code 2.1.286); follow them in this order.

1. **Find the situation.** Ask yourself (and the user only if it changes the skill): what will the user be doing or saying when this skill should run? Write down three real requests in the user's own words. Decide the type:
   - a *task* skill produces a thing (a changelog entry, a commit message, a review of a script);
   - a *process* skill changes how Claude works (verify before saying done, check the same mistake elsewhere). A process skill is only used if the description names the situation the user is in, for example "Use when the user reports a bug, an error or a failing test". A broad description ("any non-trivial task") was never called; the situation description was called in 22 of 24 runs.
   - **Check that the trigger is in the request.** Claude picks a skill from what the user asks at the start. A rule that applies later in the work (after finishing, when a command fails, before changing many files) was picked in 2 of 48 prompts (three such skills, four ways of writing them), however it was described. For those, put the rule in `CLAUDE.md` or make the skill manual-only and call it by name, and tell the user why.
2. **Write the description from those requests.**
   - One or two sentences, under about 250 characters: "Use when the user asks to ... / reports ... / is about to ...", then what the skill does, then "Do not use for ...".
   - Use the words the user would use. Do not put commands in it ("Always call this skill"): they were ignored in 24 of 24 runs.
   - Shorter is better in a large collection: descriptions are shown from a shared budget, in folder order, and about twice as many 100-character descriptions fit as 200-character ones.
3. **Name it for what it does.** Lower-case kebab-case, the topic in the name (`changelog-entry`, not `ce2`). When a description is cut from a long list, only the name is seen: a descriptive name was still called every time, an opaque one never.
4. **Write the body as steps and rules.**
   - Numbered steps, then a short list of rules, then the output format. Style rules work best as a list of things not to do.
   - Keep it short: about 0.4 tokens per character are paid every time the skill runs. Over 12,000 characters, split it.
   - Refer only to files that exist in the skill folder, and say in the body when to read them. A pointer to a missing file went unnoticed.
5. **Manual-only for rarely used skills.** Add `disable-model-invocation: true` if the user will always call it by name or it is one of many (more than about 50): manual-only skills are not listed and use none of the listing budget, and the automatic ones keep their descriptions.
6. **Check it.** Run the audit script in this skill's `scripts` folder on the new skill folder, for example `python scripts/skill_audit.py path/to/skills`, and fix every ERROR and WARN you agree with.
7. **Test that it fires.** Write four requests that should trigger it (two with the key words, two paraphrased) and four near-misses, each with its material inside the request. Run each as `claude -p "<request>"` in a folder that contains only this skill and see whether Claude calls it. Report the counts, not an impression.

Output: the skill folder (SKILL.md and any files it refers to), the audit result, and the test counts. Say what you did not test.
