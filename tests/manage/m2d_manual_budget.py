#!/usr/bin/env python3
"""M2d: do manual-only skills use up the description budget?   python m2d_manual_budget.py -> results/m2d/raw.jsonl"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc
from m2c_cut_map import make

OUT = mc.HERE / "results" / "m2d"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "raw.jsonl"
    done = {(r["config"], r["rep"]) for r in map(json.loads, raw.read_text(encoding="utf-8").splitlines())} if raw.exists() else set()
    skills = make(400, 200)
    names = sorted(skills)
    manual = names[:300]
    probe = names[300::10]
    for config in ("B", "C"):
        for rep in (1, 2):
            if (config, rep) in done:
                continue
            prompt = ("First: write the line SEE_A000: YES if a skill named " + names[0] + " is in your list of available skills, otherwise SEE_A000: NO. Then, for each of these skills, write one line: the name, a colon, "
                      "then the first 60 characters of its description exactly as you see it; if you see only the name and no description for that skill, write NONE after the colon. Skills: " + ", ".join(probe))
            wd = mc.build(mc.WORK / f"m2d_{config}_{rep}", skills, manual=manual if config == "B" else ())
            r = mc.run_full(wd, prompt, max_turns=2, timeout=400)
            vis = {}
            for p in probe:
                m = re.search(re.escape(p) + r"\s*:\s*(.+)", r["answer"])
                vis[p] = None if not m else (not m.group(1).strip().upper().startswith("NONE"))
            see = re.search(r"SEE_A000:\s*(YES|NO)", r["answer"])
            row = {"config": config, "rep": rep, "visible": sum(1 for v in vis.values() if v), "none": sum(1 for v in vis.values() if v is False), "unknown": sum(1 for v in vis.values() if v is None),
                   "sees_a000": see.group(1) if see else None, "first_request_total": r["first_request_total"], "rate_limit": r["rate_limit"]}
            with raw.open("a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row) + "\n")
            (OUT / f"answer_{config}_{rep}.txt").write_text(r["answer"], encoding="utf-8", newline="\n")
            print(config, rep, row, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
