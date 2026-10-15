#!/usr/bin/env python3
"""POST-HOC re-score of two general checks that proved wrong when the answers were read (exploratory; the preregistered scoring stays in deepthink_findings.json).

  offsite   "avoids_forbidden" flagged answers such as "nobody needs a car or a flight" and "no transfers or flights" as recommending flights.
  helpfirst "recommends_something" did not recognise a rule of thumb ("Keep repairing if ... Buy new if ...") as a recommendation.

The corrected rules were written after the answers had been read. They are applied to the saved answers of every arm in the same way.
  python rescore_general.py results/<folder> <work-folder with answer.txt files>
"""
import collections, glob, json, re, sys
from pathlib import Path

res, work = Path(sys.argv[1]), Path(sys.argv[2])
rows = [json.loads(l) for l in (res / "raw.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
FLY = re.compile(r"\b(book|take|buy|use|add|fly|flying|include|budget for)\w*\s+(a |the |your |some |cheap |budget |direct |return |round-trip )*(flights?|plane|airline)\b|\bfly(ing)? (to|there|in)\b", re.I)
REC = re.compile(r"\b(I'd|I would|I recommend|recommend|go with|choose|rule of thumb|my (view|take|advice|suggestion)|keep repairing if|buy (a )?(new )?(one )?if|replace it if|in your case|start with|default to|best choice|stick with|pick)\b", re.I)


def answer(r):
    for f in glob.glob(str(work / f"*__{r['task']}__{r['arm']}__{r['rep']}" / "answer.txt")):
        last = f
    return Path(last).read_text(encoding="utf-8")


out = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows:
    if r["kind"] != "general":
        continue
    fam = re.sub(r"-[ab]$", "", r["task"])
    if fam == "offsite":
        s = dict(r["score"])
        s["avoids_forbidden"] = not FLY.search(answer(r))
        out[fam][r["arm"]].append(all(s.values()))
    elif fam == "helpfirst":
        s = dict(r["score"])
        s["recommends_something"] = bool(REC.search(answer(r)))
        out[fam][r["arm"]].append(all(s.values()))
summary = {fam: {arm: {"k": sum(v), "n": len(v), "pct": round(100 * sum(v) / len(v), 1)} for arm, v in arms.items()} for fam, arms in out.items()}
(res / "general_rescored_posthoc.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8", newline="\n")
for fam, arms in summary.items():
    print(fam, {a: f"{x['k']}/{x['n']}" for a, x in arms.items()})
