#!/usr/bin/env python3
"""Scores prediction_part19.md against results/.   python analyze_part19.py"""
import json, math, statistics as st
from pathlib import Path

R = Path(__file__).resolve().parent / "results"
gen = [json.loads(l) for l in (R / "raw_gen.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
trig = [json.loads(l) for l in (R / "raw_trig.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
ARMS = ["plain", "creator", "writer", "writer-forced"]


def wilson(k, n, z=1.96):
    if not n:
        return [0, 0]
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(100 * max(0, c - h), 1), round(100 * min(1, c + h), 1)]


def rate(x, f):
    k = sum(1 for r in x if f(r)); n = len(x)
    return {"k": k, "n": n, "pct": round(100 * k / n, 1) if n else None, "ci": wilson(k, n)}


T = {}
for a in ARMS:
    g = [r for r in gen if r["arm"] == a]
    row = {"skills_found": f"{sum(r['found'] for r in g)}/{len(g)}"}
    for ty in ("task", "process"):
        pos = [r for r in trig if r["arm"] == a and r["type"] == ty and r["polarity"] == "pos"]
        row[f"recall_{ty}"] = rate(pos, lambda r: r["hit"])
    neg = [r for r in trig if r["arm"] == a and r["polarity"] == "neg"]
    row["false_trigger"] = rate(neg, lambda r: r["hit"] or r["other_skill"])
    row["median_desc_chars"] = st.median([r["description_chars"] for r in g if r["found"]])
    row["audit_errors_mean"] = round(st.mean([r["audit"]["errors"] for r in g if r["audit"]]), 2)
    row["audit_warns_mean"] = round(st.mean([r["audit"]["warns"] for r in g if r["audit"]]), 2)
    row["mean_output_tokens"] = round(st.mean([r["output_tokens"] for r in g if r["output_tokens"]]))
    T[a] = row
called = lambda arm, name: sum(1 for r in gen if r["arm"] == arm and name in [str(s) for s in r["skill_calls"]])
C = []
C.append(("W1", "skill-writer called in 6+ of 10 (writer); skill-creator in 4+ of 10 (creator)", called("writer", "skill-writer") >= 6 and called("creator", "skill-creator") >= 4,
          {"writer": called("writer", "skill-writer"), "creator": called("creator", "skill-creator")}))
pw = lambda arms, ty: rate([r for r in trig if r["arm"] in arms and r["type"] == ty and r["polarity"] == "pos"], lambda r: r["hit"])
w_p, p_p = pw(("writer", "writer-forced"), "process"), pw(("plain",), "process")
C.append(("W2", "process skills: writer arms pooled at least 20 points above plain", w_p["pct"] - p_p["pct"] >= 20, {"writer_pooled": w_p, "plain": p_p}))
ok3 = all(abs(T[a]["recall_task"]["pct"] - T["plain"]["recall_task"]["pct"]) <= 10 for a in ("writer", "writer-forced"))
C.append(("W3", "task skills: writer and writer-forced within 10 points of plain", ok3, {a: T[a]["recall_task"]["pct"] for a in ARMS}))
C.append(("W4", "false triggers at most 10% in every arm", all(T[a]["false_trigger"]["pct"] <= 10 for a in ARMS), {a: T[a]["false_trigger"] for a in ARMS}))
ok5 = all(T[a]["audit_errors_mean"] == 0 and T[a]["audit_warns_mean"] <= 0.5 for a in ("writer", "writer-forced")) and T["plain"]["audit_warns_mean"] >= 1.0
C.append(("W5", "audit: writer arms no ERROR and at most 0.5 WARN each; plain at least 1.0 WARN each", ok5, {a: (T[a]["audit_errors_mean"], T[a]["audit_warns_mean"]) for a in ARMS}))
ok6 = all(T[a]["median_desc_chars"] <= 300 and T[a]["median_desc_chars"] < T["plain"]["median_desc_chars"] for a in ("writer", "writer-forced"))
C.append(("W6", "median description at most 300 characters and shorter than plain (writer arms)", ok6, {a: T[a]["median_desc_chars"] for a in ARMS}))
C.append(("W7", "output tokens of the writer arms at most 2x plain", all(T[a]["mean_output_tokens"] <= 2 * T["plain"]["mean_output_tokens"] for a in ("writer", "writer-forced")), {a: T[a]["mean_output_tokens"] for a in ARMS}))
out = {"arms": T, "clauses": [{"id": i, "text": t, "verdict": "holds" if ok else "fails", "evidence": e} for i, t, ok, e in C]}
(R / "part19_findings.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
for a in ARMS:
    t = T[a]
    print(f"{a:14s} found {t['skills_found']} recall task {t['recall_task']['k']}/{t['recall_task']['n']} ({t['recall_task']['pct']}%) process {t['recall_process']['k']}/{t['recall_process']['n']} ({t['recall_process']['pct']}% {t['recall_process']['ci']}) false {t['false_trigger']['k']}/{t['false_trigger']['n']} desc {t['median_desc_chars']} audit E{t['audit_errors_mean']} W{t['audit_warns_mean']} out {t['mean_output_tokens']}")
for i, t, ok, e in C:
    print(f"{i} {'holds' if ok else 'fails':6s} {t}\n      {e}")
print(sum(1 for c in C if c[2]), "hold,", sum(1 for c in C if not c[2]), "fail")
