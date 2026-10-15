#!/usr/bin/env python3
"""M5: documented behaviours of skills in a project (see prediction_m5.md).   python m5_docs_probes.py  -> results/m5/observations.json"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc

OUT = mc.HERE / "results" / "m5"
CL = mc.suite_skills(["changelog-entry"])["changelog-entry"]   # (description, body)
ALLOW = ["--permission-mode", "acceptEdits", "--allowedTools", "Read,Glob,Grep,Write,Edit,Skill,Bash(ls *),Bash(cat *)"]


def skill_file(name, desc, extra="", body="Write the entry in Keep a Changelog format."):
    fm = f"---\nname: {name}\n" + (f"description: {desc}\n" if desc is not None else "") + extra + "---\n\n" + body + "\n"
    return {f".claude/skills/{name}/SKILL.md": fm}


def run(tag, files, prompt, cwd_sub="", full=True, extra=()):
    wd = mc.build(mc.WORK / f"m5_{tag}", {}, files=files)
    if cwd_sub:
        wd = wd / cwd_sub
    r = mc.run_full(wd, prompt, max_turns=5, timeout=300, extra_args=list(extra)) if full else None
    return r


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    obs = {}
    desc = CL[0]
    base_files = skill_file("changelog-entry", desc)
    # M5.1 disableBundledSkills
    a = run("d1a", base_files, "x")
    b = run("d1b", {**base_files, ".claude/settings.json": json.dumps({"disableBundledSkills": True})}, "x")
    obs["M5.1"] = {"control_skills": len(a["init_skills"]), "setting_skills": len(b["init_skills"]), "setting_skill_names": b["init_skills"], "control_first_request": a["first_request_total"], "setting_first_request": b["first_request_total"]}
    # M5.2 skillOverrides
    for mode in ("on", "name-only", "off"):
        r = run(f"d2{mode}", {**base_files, ".claude/settings.json": json.dumps({"skillOverrides": {"changelog-entry": mode}})},
                "Quote exactly the description of the skill changelog-entry from your list of available skills. If it is not in the list, or has no description, say NOT VISIBLE.")
        obs.setdefault("M5.2", {})[mode] = {"first_request": r["first_request_total"], "in_init": "changelog-entry" in r["init_skills"], "answer": r["answer"][:200]}
    # M5.3 when_to_use
    short = "Use when the user asks for a changelog entry."
    wtu = "Also use it for release sections, version headings, CHANGELOG.md files, Keep a Changelog layouts, and requests to tidy or reformat an existing changelog. " * 2
    a = run("d3a", skill_file("wtu-test", short), "x")
    b = run("d3b", skill_file("wtu-test", short, extra=f"when_to_use: {wtu.strip()}\n"), "x")
    obs["M5.3"] = {"without": a["first_request_total"], "with": b["first_request_total"], "added": b["first_request_total"] - a["first_request_total"], "when_to_use_chars": len(wtu.strip())}
    # M5.4 description omitted
    r = run("d4", skill_file("nodesc-test", None, body="Convert a cURL command into Python requests code.\n\nMore text follows."),
            "Quote exactly the description of the skill nodesc-test from your list of available skills, or say NOT VISIBLE.")
    obs["M5.4"] = {"answer": r["answer"][:300]}
    # M5.5 user-invocable false
    empty = run("d5e", {}, "x")
    f5 = skill_file("changelog-entry", desc, extra="user-invocable: false\n")
    r5 = run("d5", f5, "x")
    obs["M5.5"] = {"listing_added": r5["first_request_total"] - empty["first_request_total"], "natural_calls": []}
    for i in range(2):
        wd = mc.build(mc.WORK / "m5_d5n", {}, files=f5)
        obs["M5.5"]["natural_calls"].append(mc.first_move(wd, "Write the changelog entry for 2.3.0: added dark mode setting, fixed login redirect loop, removed the old export endpoint.")["decision"])
    # M5.6 nested skills
    files6 = {**skill_file("pkg-skill", "Use when the user asks about the pkg folder."), }
    files6 = {f"pkg/{k}": v for k, v in files6.items()}
    files6["pkg/a.txt"] = "hello from pkg\n"
    r = run("d6", files6, "Step 1: list only the names of the skills available to you right now, comma separated, after the label STEP1:. Step 2: read the file pkg/a.txt. Step 3: list only the names of the skills available to you now, after the label STEP3:.")
    obs["M5.6"] = {"answer": r["answer"][:600]}
    # M5.7 mention of a manual-only skill
    f7 = skill_file("changelog-entry", desc, extra="disable-model-invocation: true\n")
    calls_named, calls_plain = [], []
    for i in range(2):
        wd = mc.build(mc.WORK / "m5_d7", {}, files=f7)
        calls_named.append(mc.first_move(wd, "Use the changelog-entry skill to write the changelog entry for 2.3.0: added dark mode setting, removed the old export endpoint.")["decision"])
        wd = mc.build(mc.WORK / "m5_d7", {}, files=f7)
        calls_plain.append(mc.first_move(wd, "Write the changelog entry for 2.3.0: added dark mode setting, removed the old export endpoint.")["decision"])
    obs["M5.7"] = {"named": calls_named, "plain": calls_plain}
    # M5.8 model override
    r = run("d8", skill_file("modeltest", "Use when the user says modeltest.", extra="model: haiku\n", body="Reply with the single word PONG."), "/modeltest")
    obs["M5.8"] = {"models": r["models"], "answer": r["answer"][:100]}
    # M5.9 context fork
    r = run("d9", skill_file("forktest", "Use when the user says forktest.", extra="context: fork\n", body="List the files in the current folder and report their names."), "/forktest")
    obs["M5.9"] = {"tools": [t[0] for t in r["tools"]], "answer": r["answer"][:200]}
    # M5.10 live reload
    r = run("d10", {}, "Create the file .claude/skills/late/SKILL.md containing a valid skill named late with the description 'Use when the user says banana' and a one-line body. Then call the Skill tool with skill late. Finally say exactly WORKED if the Skill call succeeded or FAILED followed by the error text.", extra=ALLOW)
    obs["M5.10"] = {"tools": [t[0] for t in r["tools"]], "answer": r["answer"][:300]}
    # M5.11 same name in parent and child
    files11 = {**skill_file("dup", "ROOT-VERSION of the dup skill."), **{f"pkg/{k}": v for k, v in skill_file("dup", "CHILD-VERSION of the dup skill.").items()}, "pkg/a.txt": "x\n"}
    r = run("d11", files11, "Quote exactly the description of the skill dup from your list of available skills.", cwd_sub="pkg")
    obs["M5.11"] = {"answer": r["answer"][:200]}
    (OUT / "observations.json").write_text(json.dumps(obs, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(obs, indent=1)[:6000])


if __name__ == "__main__":
    main()
