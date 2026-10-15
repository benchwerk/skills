#!/usr/bin/env python3
"""Version canary (M7): five first-request measurements that take a few minutes on any Claude Code version, to notice when an update moves the numbers.

  CLAUDE_CONFIG_DIR=<isolated, logged in> CLAUDE_BIN=<claude executable> python canary.py [--model claude-sonnet-5-5[1m]]

Measures the size of the first request (input + cache creation + cache read) for:
  empty        a project with no skills of its own
  one          one automatic skill (changelog-entry of the suite)
  suite        the 15 skills of the suite
  manual       the same one skill with disable-model-invocation: true (expected: no more than the empty session)
  invoked      the one skill called by name (/changelog-entry): adds its body
It prints a table and writes canary_<version>.json next to this file. Compare with the table in RESULTS.md (Claude Code 2.1.284 and 2.1.286, Sonnet 5.5)."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc


def total(wd, prompt, model):
    mc.MODEL = model
    r = mc.run_full(wd, prompt, max_turns=1, timeout=180)
    return r["first_request_total"], r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-sonnet-5-5[1m]")
    a = ap.parse_args()
    version = subprocess.run([mc.exe(), "--version"], capture_output=True, text=True).stdout.strip().split()[0]
    suite = mc.suite_skills()
    one = {"changelog-entry": suite["changelog-entry"]}
    rows = {}
    for name, skills, manual, prompt in (("empty", {}, (), "x"), ("one", one, (), "x"), ("suite", suite, (), "x"),
                                         ("manual", one, ("changelog-entry",), "x"), ("invoked", one, (), "/changelog-entry")):
        wd = mc.build(mc.WORK / "canary", skills, manual=manual)   # one fixed folder: the path is part of the prompt, so a different folder name changes the token count
        if not rows:   # the first call in a fresh folder reads 88 tokens low (seen on 2.1.284 and 2.1.286); discard it
            total(wd, prompt, a.model)
        first, _ = total(wd, prompt, a.model)
        second, _ = total(wd, prompt, a.model)
        if first != second:
            print(f"  WARNING: {name} did not repeat ({first} then {second}); the second value is reported")
        rows[name] = second
    out = {"claude_code": version, "model": a.model, "first_request_tokens": rows,
           "added": {"one_skill_listing": rows["one"] - rows["empty"], "suite_listing": rows["suite"] - rows["empty"], "manual_only": rows["manual"] - rows["empty"],
                     "invocation_over_listing": rows["invoked"] - rows["one"]}}
    (Path(__file__).resolve().parent / f"canary_{version}.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"Claude Code {version}, {a.model}")
    for k, v in rows.items():
        print(f"  {k:8s} {v:7d}")
    print("  added:", out["added"])


if __name__ == "__main__":
    main()
