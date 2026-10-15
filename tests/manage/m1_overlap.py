#!/usr/bin/env python3
"""M1: skills with similar descriptions. Both skills of a pair are installed (nothing else); B's description is at three levels; 8 prompts per pair
(4 that belong to A, 4 to B), 2 runs. A call stops at the model's first decision.   python m1_overlap.py [--stop-at 0.90] -> results/m1/raw.jsonl"""
import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc

OUT = mc.HERE / "results" / "m1"
PAIRS = json.loads((mc.HERE / "m1_pairs.json").read_text(encoding="utf-8"))["pairs"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stop-at", type=float, default=0.90)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "raw.jsonl"
    done = {(r["pair"], r["level"], r["owner"], r["prompt_id"], r["rep"]) for r in map(json.loads, raw.read_text(encoding="utf-8").splitlines())} if raw.exists() else set()
    suite = mc.suite_skills()
    plan = [(i, level, owner, k, rep) for i in range(len(PAIRS)) for level in ("distinct", "adjacent", "near") for owner in ("a", "b") for k in range(4) for rep in (1, 2)]
    random.Random(5).shuffle(plan)
    for i, level, owner, k, rep in plan:
        p = PAIRS[i]
        key = (p["a"], level, owner, k, rep)
        if key in done:
            continue
        skills = {p["a"]: suite[p["a"]], p["b"]: (suite[p["b"]][0] if level == "adjacent" else p["b_" + level], suite[p["b"]][1])}
        wd = mc.build(mc.WORK / "m1", skills)
        prompt = p[owner + "_prompts"][k]
        want = p[owner]
        r = mc.first_move(wd, prompt)
        d = r["decision"]
        row = {"pair": p["a"], "level": level, "owner": owner, "prompt_id": k, "rep": rep, "wanted": want, "decision": d, "correct": d == "skill:" + want,
               "wrong_skill": d.startswith("skill:") and d != "skill:" + want, "none": not d.startswith("skill:"), "rate_limit": r["rate_limit"], "seconds": r["seconds"]}
        with raw.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row) + "\n")
        print(p["a"], level, owner, k, rep, "->", d, r["rate_limit"] and r["rate_limit"].get("five_hour"), flush=True)
        if d == "timeout":
            print("STOP: timeout")
            return 3
        if r["rate_limit"] and (r["rate_limit"].get("five_hour") or 0) >= a.stop_at:
            print("STOP: meter at the limit")
            return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
