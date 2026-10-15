#!/usr/bin/env python3
"""M2b: does a skill that shows only its name still get picked?   python m2b_name_only.py [--stop-at 0.90] -> results/m2b/raw.jsonl"""
import argparse, json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc
from m2c_cut_map import make

OUT = mc.HERE / "results" / "m2b"
P = json.loads((mc.HERE / "m2b_prompts.json").read_text(encoding="utf-8"))["targets"]
OPAQUE = {"changelog-entry": "w7k2", "sql-migration-review": "q3m9", "bash-script-safety-review": "z5r1"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stop-at", type=float, default=0.90)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "raw.jsonl"
    done = {(r["target"], r["pos"], r["name_style"], r["prompt_id"], r["rep"]) for r in map(json.loads, raw.read_text(encoding="utf-8").splitlines())} if raw.exists() else set()
    suite = mc.suite_skills()
    fillers = make(400, 200)
    fnames = sorted(fillers)
    plan = [(t, pos, ns, i, rep) for t in P for pos in ("early", "late") for ns in ("descriptive", "opaque") for i in range(4) for rep in (1, 2)]
    random.Random(99).shuffle(plan)
    for t, pos, ns, i, rep in plan:
        if (t, pos, ns, i, rep) in done:
            continue
        idx = 10 if pos == "early" else 390
        tname = f"a{idx:03d}-" + (t if ns == "descriptive" else OPAQUE[t])
        skills = {n: d for n, d in fillers.items() if not n.startswith(f"a{idx:03d}-")}
        skills[tname] = suite[t]
        wd = mc.build(mc.WORK / "m2b", skills)
        r = mc.first_move(wd, P[t][i])
        row = {"target": t, "pos": pos, "name_style": ns, "prompt_id": i, "rep": rep, "skill_name": tname, "decision": r["decision"], "hit": r["decision"] == "skill:" + tname,
               "other_skill": r["decision"].startswith("skill:") and r["decision"] != "skill:" + tname, "rate_limit": r["rate_limit"], "seconds": r["seconds"]}
        with raw.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row) + "\n")
        print(t, pos, ns, i, rep, "->", r["decision"], r["rate_limit"] and r["rate_limit"].get("five_hour"), flush=True)
        if r["decision"] == "timeout":
            print("STOP: timeout")
            return 3
        if r["rate_limit"] and (r["rate_limit"].get("five_hour") or 0) >= a.stop_at:
            print("STOP: meter at the limit")
            return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
