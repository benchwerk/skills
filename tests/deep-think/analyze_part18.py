#!/usr/bin/env python3
"""Scores prediction_part18.md against results/<folder>/raw.jsonl.   python analyze_part18.py results/<folder>"""
import json, math, sys
from pathlib import Path

d = Path(sys.argv[1])
rows = [json.loads(l) for l in (d / "raw.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
ARMS = ["d0", "d1", "d2", "d3", "d4"]
cod = [r for r in rows if r["kind"] == "coding"]
gen = [r for r in rows if r["kind"] == "general"]


def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(100 * max(0, c - h), 1), round(100 * min(1, c + h), 1)]


def R(x, f):
    k = sum(1 for r in x if f(r)); n = len(x)
    return {"k": k, "n": n, "pct": round(100 * k / n, 1) if n else None, "ci": wilson(k, n) if n else None}


T = {}
for a in ARMS:
    x = [r for r in cod if r["arm"] == a]
    g = [r for r in gen if r["arm"] == a]
    T[a] = {"called": R(x, lambda r: r["triggered"]), "second_fixed": R(x, lambda r: r["score"]["second_fixed"]), "false_trigger": R(g, lambda r: r["triggered"]),
            "out_tokens": round(sum(r["output_tokens"] for r in x) / len(x)), "turns": round(sum(r["turns"] for r in x) / len(x), 1),
            "cannot_fail": R([r for r in x if r["score"]["has_cannot_fail_test"]], lambda r: r["score"]["reported_cannot_fail_test"])}
called = [r for r in cod if r["triggered"]]
not_called = [r for r in cod if not r["triggered"]]
pc = lambda a, k: T[a][k]["pct"]
C = []
C.append(("P18.1", "d0 called in at most 10%", pc("d0", "called") <= 10, pc("d0", "called")))
C.append(("P18.2", "d2 at least 75%; d1 and d4 at least 60%", pc("d2", "called") >= 75 and pc("d1", "called") >= 60 and pc("d4", "called") >= 60, {a: pc(a, "called") for a in ("d1", "d2", "d4")}))
C.append(("P18.3", "d3 at least 30% and at least 15 points below d2", pc("d3", "called") >= 30 and pc("d3", "called") <= pc("d2", "called") - 15, {"d2": pc("d2", "called"), "d3": pc("d3", "called")}))
a_, b_ = R(called, lambda r: r["score"]["second_fixed"]), R(not_called, lambda r: r["score"]["second_fixed"])
C.append(("P18.4", "called runs fix the second instance 20+ points more often (15+ called runs)", len(called) >= 15 and a_["pct"] - b_["pct"] >= 20, {"called": a_, "not_called": b_}))
mt = lambda x: sum(r["output_tokens"] for r in x) / len(x) if x else float("nan")
C.append(("P18.5", "called runs use 1.5x the output tokens of not-called runs", mt(called) >= 1.5 * mt(not_called), {"called": round(mt(called)), "not_called": round(mt(not_called)), "ratio": round(mt(called) / mt(not_called), 2)}))
ft = {a: T[a]["false_trigger"]["k"] for a in ARMS}
C.append(("P18.6", "false triggers (8 runs per arm): d1, d2, d3 at most 1; d0, d4 at most 2", all(ft[a] <= 1 for a in ("d1", "d2", "d3")) and all(ft[a] <= 2 for a in ("d0", "d4")), ft))
best = max(ARMS, key=lambda a: pc(a, "called"))
C.append(("P18.7", "the arm with the highest call rate is d2 or d4", best in ("d2", "d4"), {"best": best, "rates": {a: pc(a, "called") for a in ARMS}}))
out = {"arms": T, "pooled": {"called_runs": len(called), "not_called_runs": len(not_called)}, "clauses": [{"id": i, "text": t, "verdict": "holds" if ok else "fails", "evidence": e} for i, t, ok, e in C]}
(d / "part18_findings.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
for a in ARMS:
    t = T[a]
    print(f"{a}: called {t['called']['k']}/{t['called']['n']} ({t['called']['pct']}%, {t['called']['ci']})  second {t['second_fixed']['k']}/24 ({t['second_fixed']['pct']}%)  false {t['false_trigger']['k']}/{t['false_trigger']['n']}  out {t['out_tokens']} turns {t['turns']} cannot-fail {t['cannot_fail']['k']}/{t['cannot_fail']['n']}")
for i, t, ok, e in C:
    print(f"{i} {'holds' if ok else 'fails':6s} {t}  {e}")
print(sum(1 for c in C if c[2]), "hold,", sum(1 for c in C if not c[2]), "fail")
