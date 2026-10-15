#!/usr/bin/env python3
"""M2c: where does the description cut fall?   python m2c_cut_map.py  -> results/m2c/raw.jsonl"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc

OUT = mc.HERE / "results" / "m2c"
CONFIGS = [(100, 200), (200, 200), (300, 200), (400, 200), (400, 100)]


def make(n, length):
    """n synthetic skills named a000, a001, ... (folder order is numeric order), every description exactly `length` characters"""
    base = mc.synthetic(n, seed=777, min_len=length, max_len=length, prefix="a")
    out = {}
    for i, (old, d) in enumerate(base.items()):
        out[f"a{i:03d}-" + old.split("-", 1)[1]] = d
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "raw.jsonl"
    done = {(r["n"], r["length"], r["rep"]) for r in map(json.loads, raw.read_text(encoding="utf-8").splitlines())} if raw.exists() else set()
    for n, length in CONFIGS:
        for rep in (1, 2):
            if (n, length, rep) in done:
                continue
            skills = make(n, length)
            names = sorted(skills)
            probe = names[::10]
            prompt = ("For each of these skills, write one line: the name, a colon, then the first 60 characters of its description exactly as you see it in your list of available skills; "
                      "if you see only the name and no description for that skill, write NONE after the colon. Skills: " + ", ".join(probe))
            wd = mc.build(mc.WORK / f"m2c_{n}_{length}_{rep}", skills)
            r = mc.run_full(wd, prompt, max_turns=2, timeout=400)
            vis = {}
            for p in probe:
                m = re.search(re.escape(p) + r"\s*:\s*(.+)", r["answer"])
                vis[p] = None if not m else (not m.group(1).strip().upper().startswith("NONE"))
            seq = [vis[p] for p in probe]
            seen_gap, exceptions = False, 0
            for v in seq:
                if v is False:
                    seen_gap = True
                elif v is True and seen_gap:
                    exceptions += 1
            row = {"n": n, "length": length, "rep": rep, "probe_n": len(probe), "visible": sum(1 for v in seq if v), "unknown": sum(1 for v in seq if v is None),
                   "last_visible_index": max([i * 10 for i, v in enumerate(seq) if v], default=-1), "first_none_index": min([i * 10 for i, v in enumerate(seq) if v is False], default=None),
                   "prefix_exceptions": exceptions, "first_request_total": r["first_request_total"], "rate_limit": r["rate_limit"],
                   "sequence": "".join("V" if v else ("." if v is False else "?") for v in seq)}
            with raw.open("a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row) + "\n")
            (OUT / f"answer_{n}_{length}_{rep}.txt").write_text(r["answer"], encoding="utf-8", newline="\n")
            print(f"N={n} len={length} rep{rep}: {row['sequence']}  first request {row['first_request_total']}", flush=True)
            rl = r["rate_limit"]
            if rl and (rl.get("five_hour") or 0) >= 0.90:
                print("STOP: meter at the limit")
                return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
