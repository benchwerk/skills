#!/usr/bin/env python3
"""Part 19: skills written by Claude with and without skill-writer, then tested for whether they get picked.
  python run_part19.py [--stop-at 0.90] [--phase gen,trig]     resumes by itself      -> results/raw_gen.jsonl, results/raw_trig.jsonl"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "manage"))
import manage_common as mc  # noqa: E402

REPO = HERE.parents[1]
TASKS = json.loads((HERE / "part19_tasks.json").read_text(encoding="utf-8"))["tasks"]
ARMS = ["plain", "creator", "writer", "writer-forced"]
RES = HERE / "results"
CREATOR = Path(__file__).resolve().parents[4] / "videos/004-skill-context-cost/workload/src/anthropics__skills/skills/skill-creator"   # the pinned clone in the main study
ALLOWED = "Read,Glob,Grep,Edit,Write,Skill,Bash(python *),Bash(python3 *),Bash(ls *),Bash(cat *),Bash(mkdir *),Bash(pwd),Bash(echo *)"


def prompt_for(arm, t):
    base = f"Write a Claude Code skill: {t['request']} Save it as out/{t['slug']}/SKILL.md (the folder out/ exists). Do not ask questions. Do not run the claude command."
    return ("/skill-writer " if arm == "writer-forced" else "") + base


def build_gen(arm, run_dir):
    wd = mc.build(run_dir, {})
    (wd / "out").mkdir()
    if arm == "creator":
        shutil.copytree(CREATOR, wd / ".claude" / "skills" / "skill-creator")
    elif arm in ("writer", "writer-forced"):
        shutil.copytree(REPO / "skill-writer", wd / ".claude" / "skills" / "skill-writer")
    return wd


def audit(folder):
    p = subprocess.run([sys.executable, str(REPO / "skill-writer" / "scripts" / "skill_audit.py"), str(folder)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    lines = p.stdout.splitlines()
    return {"errors": sum(1 for l in lines if l.strip().startswith("ERROR")), "warns": sum(1 for l in lines if l.strip().startswith("WARN")),
            "lines": [l.strip() for l in lines if l.strip().startswith(("ERROR", "WARN"))]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stop-at", type=float, default=0.90)
    ap.add_argument("--phase", default="gen,trig")
    a = ap.parse_args()
    RES.mkdir(exist_ok=True)
    (RES / "skills").mkdir(exist_ok=True)
    gen_f, trig_f = RES / "raw_gen.jsonl", RES / "raw_trig.jsonl"
    load = lambda f: [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()] if f.exists() else []
    gdone = {(r["arm"], r["task"]) for r in load(gen_f)}
    tdone = {(r["arm"], r["task"], r["prompt_id"]) for r in load(trig_f) if r["decision"] != "timeout"}

    def meter(rl):
        if rl and (rl.get("five_hour") or 0) >= a.stop_at:
            print(f"STOP: meter {rl.get('five_hour')}")
            sys.exit(3)

    if "gen" in a.phase:
        for t in TASKS:
            for arm in ARMS:
                if (arm, t["id"]) in gdone:
                    continue
                run_dir = mc.WORK / f"p19_{arm}_{t['id']}"
                wd = build_gen(arm, run_dir)
                r = mc.run_full(wd, prompt_for(arm, t), max_turns=30, timeout=900, extra_args=["--permission-mode", "acceptEdits", "--allowedTools", ALLOWED])
                src = wd / "out" / t["slug"]
                dest = RES / "skills" / arm / t["slug"]
                if dest.exists():
                    mc.rm_tree(dest)
                found = src.exists()
                if found:
                    shutil.copytree(src, dest)
                called = [json.loads(x[1])["skill"] if x[1].startswith("{") and "skill" in x[1] else x[1] for x in r["tools"] if x[0] == "Skill"] if r["tools"] else []
                text = (dest / "SKILL.md").read_text(encoding="utf-8-sig") if found and (dest / "SKILL.md").exists() else ""
                m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
                desc = re.search(r"^description:\s*(.*)$", m.group(1), re.M).group(1).strip() if m and re.search(r"^description:", m.group(1), re.M) else ""
                row = {"arm": arm, "task": t["id"], "type": t["type"], "found": found, "skill_calls": called, "description_chars": len(desc), "description": desc,
                       "output_tokens": r["usage"].get("output_tokens"), "tool_calls": len(r["tools"]), "audit": audit(dest) if found else None, "rate_limit": r["rate_limit"]}
                with gen_f.open("a", encoding="utf-8", newline="\n") as f:
                    f.write(json.dumps(row) + "\n")
                print("gen", arm, t["id"], "found" if found else "MISSING", "skills called:", called, "desc", len(desc), r["rate_limit"] and r["rate_limit"].get("five_hour"), flush=True)
                meter(r["rate_limit"])
    if "trig" in a.phase:
        for t in TASKS:
            for arm in ARMS:
                skill_dir = RES / "skills" / arm / t["slug"]
                if not (skill_dir / "SKILL.md").exists():
                    continue
                txt = (skill_dir / "SKILL.md").read_text(encoding="utf-8-sig")
                nm = re.search(r"^name:\s*(\S+)", txt, re.M)
                name = nm.group(1).strip("'\"") if nm else t["slug"]
                for pol in ("pos", "neg"):
                    for i, pr in enumerate(t[pol]):
                        pid = f"{pol}{i}"
                        if (arm, t["id"], pid) in tdone:
                            continue
                        wd = mc.WORK / "p19_trig"
                        if wd.exists():
                            mc.rm_tree(wd)
                        (wd / ".claude" / "skills").mkdir(parents=True)
                        shutil.copytree(skill_dir, wd / ".claude" / "skills" / name)
                        r = mc.first_move(wd, pr)
                        row = {"arm": arm, "task": t["id"], "type": t["type"], "prompt_id": pid, "polarity": pol, "skill_name": name, "decision": r["decision"],
                               "hit": r["decision"] == "skill:" + name, "other_skill": r["decision"].startswith("skill:") and r["decision"] != "skill:" + name, "rate_limit": r["rate_limit"]}
                        with trig_f.open("a", encoding="utf-8", newline="\n") as f:
                            f.write(json.dumps(row) + "\n")
                        print("trig", arm, t["id"], pid, r["decision"], r["rate_limit"] and r["rate_limit"].get("five_hour"), flush=True)
                        if r["decision"] == "timeout":
                            print("STOP: timeout")
                            return 3
                        meter(r["rate_limit"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
