#!/usr/bin/env python3
"""M5b: redo of M5.6, M5.7, M5.10 (see prediction_part16.md).   python m5b_redo.py -> results/m5/observations_b.json"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc
from m5_docs_probes import skill_file, CL

OUT = mc.HERE / "results" / "m5"
obs = {}
files6 = {f"pkg/{k}": v for k, v in skill_file("pkg-skill", "Use when the user asks about the pkg folder.").items()}
files6["pkg/a.txt"] = "hello from pkg\n"
wd = mc.build(mc.WORK / "m5b_6", {}, files=files6)
r = mc.run_full(wd, "Read the file pkg/a.txt. Then list only the names of the skills available to you now, comma separated, after the label NOW:.", max_turns=5, timeout=300,
                extra_args=["--permission-mode", "acceptEdits", "--allowedTools", "Read,Glob,Grep"])
obs["M5.6b"] = {"in_start_list": "pkg-skill" in r["init_skills"], "start_list_size": len(r["init_skills"]), "after_read_answer_has_it": "pkg-skill" in r["answer"], "answer": r["answer"][-300:]}
f7 = skill_file("changelog-entry", CL[0], extra="disable-model-invocation: true\n")
obs["M5.7b"] = []
for i in range(2):
    wd = mc.build(mc.WORK / "m5b_7", {}, files=f7)
    obs["M5.7b"].append(mc.first_move(wd, "Please do this with /changelog-entry: write the changelog entry for 2.3.0, added dark mode setting, removed the old export endpoint.")["decision"])
wd = mc.build(mc.WORK / "m5b_10", {})
r = mc.run_full(wd, "Run a python command that creates the file .claude/skills/late/SKILL.md with the text: three dashes, a line name: late, a line description: Use when the user says banana, three dashes, a blank line, then Reply BANANA. Then call the Skill tool with skill late. Finally say exactly WORKED if the Skill call succeeded or FAILED followed by the error text.",
                max_turns=6, timeout=300, extra_args=["--permission-mode", "acceptEdits", "--allowedTools", "Skill,Bash(python *),Bash(python3 *),Bash(ls *),Bash(cat *),Read"])
obs["M5.10b"] = {"tools": [t[0] for t in r["tools"]], "answer": r["answer"][:300]}
(OUT / "observations_b.json").write_text(json.dumps(obs, indent=1) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(obs, indent=1))
