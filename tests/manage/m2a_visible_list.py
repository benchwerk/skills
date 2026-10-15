#!/usr/bin/env python3
"""M2a: what does Claude see of a long skill list?  python m2a_visible_list.py [--reps 3]  -> results/m2a/raw.jsonl"""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc

OUT = mc.HERE / "results" / "m2a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--stop-at", type=float, default=0.90)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "raw.jsonl"
    done = {(r["n"], r["rep"]) for r in map(json.loads, raw.read_text(encoding="utf-8").splitlines())} if raw.exists() else set()
    suite = mc.suite_skills()
    for n in (50, 100, 200, 400):
        for rep in range(1, a.reps + 1):
            if (n, rep) in done:
                continue
            syn = mc.synthetic(n - len(suite), seed=4242, prefix="x")
            skills = {**{k: v for k, v in suite.items()}, **syn}
            names = sorted(skills)
            picks = [names[0], names[len(names) // 4], names[len(names) // 2], names[3 * len(names) // 4], names[-1], "changelog-entry"]
            picks = list(dict.fromkeys(picks))[:6]
            prompt = ("List every skill name that is available to you, one per line, exactly as written and in the order you see them, with no other text between the first "
                      "and the last name. Then write the line ===. Then, for each of these skills, write the name, a colon and its description quoted exactly as you see it; "
                      "if you can only see part of a description, quote what you see and write [cut] after it: " + ", ".join(picks))
            wd = mc.build(mc.WORK / f"m2a_{n}_{rep}", skills)
            r = mc.run_full(wd, prompt, max_turns=2, timeout=400)
            ans = r["answer"]
            head, _, tail = ans.partition("===")
            listed = [l.strip().strip("-*` ") for l in head.splitlines() if re.fullmatch(r"[\w.-]+", l.strip().strip("-*` "))]
            quoted = {}
            for p in picks:
                m = re.search(re.escape(p) + r"\s*:\s*(.+)", tail)
                quoted[p] = m.group(1).strip().strip('"`') if m else None
            row = {"n": n, "rep": rep, "installed": len(skills), "listed": len(listed), "listed_valid": sum(1 for x in listed if x in skills), "order_ok_pairs": sum(1 for x, y in zip(listed, listed[1:]) if x < y),
                   "pairs": max(0, len(listed) - 1), "picks": picks, "installed_len": {p: len(skills[p] if isinstance(skills[p], str) else skills[p][0]) for p in picks},
                   "quoted_len": {p: (len(q) if q else None) for p, q in quoted.items()}, "exact": {p: bool(quoted[p] and quoted[p] == (skills[p] if isinstance(skills[p], str) else skills[p][0])) for p in picks},
                   "cut_marked": {p: bool(quoted[p] and "[cut]" in quoted[p]) for p in picks}, "first_request_total": r["first_request_total"], "rate_limit": r["rate_limit"],
                   "listed_sample": listed[:3] + listed[-3:]}
            with raw.open("a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row) + "\n")
            (OUT / f"answer_{n}_{rep}.txt").write_text(ans, encoding="utf-8", newline="\n")
            rl = r["rate_limit"]
            print(f"N={n} rep{rep}: listed {row['listed_valid']}/{n}, first request {row['first_request_total']}, meter {rl and rl.get('five_hour')}", flush=True)
            if rl and ((rl.get("five_hour") or 0) >= a.stop_at):
                print("STOP: meter at the limit")
                return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
