#!/usr/bin/env python3
"""M4: a hub skill that points to a library against a flat list of the same skills.   python m4_router.py [--stop-at 0.96] -> results/m4/raw.jsonl
Configurations: flat (the 15 suite skills as automatic skills), hub (one automatic skill `dev-workflows` whose body points to the same 15 skills stored as plain folders in
.claude/library/), hubmanual (the hub plus the 15 skills as manual-only skills, to see whether the hub can call them)."""
import argparse
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc

OUT = mc.HERE / "results" / "m4"
P = json.loads((mc.HERE / "m2b_prompts.json").read_text(encoding="utf-8"))["targets"]
NEG = ["Explain the difference between a mutex and a semaphore.", "Write a Python function that returns the sum of a list of numbers.",
       "What does the HTTP status code 418 mean?", "How do I undo my last git commit but keep the changes?"]
ALLOW = ["--permission-mode", "acceptEdits", "--allowedTools", "Read,Glob,Grep,Skill"]


def short(desc):
    return re.sub(r"^Use when the user asks (to |for |whether )?", "", desc).split(". ")[0].rstrip(".")


def hub_skill(suite, manual_names=False):
    lines = [f"- {n}: {short(d)}. " + (f"Call the skill {n}." if manual_names else f"Read .claude/library/{n}/SKILL.md and follow it.") for n, (d, b) in suite.items()]
    body = "Pick the one entry below that matches the request and follow its instruction. Do not use more than one.\n\n" + "\n".join(lines)
    desc = "Use when the user asks for one of these developer tasks: " + ", ".join(n.replace("-", " ") for n in suite) + "."
    return desc, body


def build(config, suite):
    skills, files = {}, {}
    if config == "flat":
        skills = dict(suite)
    else:
        skills["dev-workflows"] = hub_skill(suite, manual_names=(config == "hubmanual"))
        if config == "hub":
            for n, (d, b) in suite.items():
                files[f".claude/library/{n}/SKILL.md"] = f"# {n}\n\n{d}\n\n{b}\n"
        else:
            skills.update(suite)
    return mc.build(mc.WORK / "m4", skills, files=files, manual=tuple(suite) if config == "hubmanual" else ())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stop-at", type=float, default=0.96)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "raw.jsonl"
    done = {(r["config"], r["kind"], r["target"], r["prompt_id"], r["rep"]) for r in map(json.loads, raw.read_text(encoding="utf-8").splitlines())} if raw.exists() else set()
    suite = mc.suite_skills()
    idle_f = OUT / "idle.json"
    if not idle_f.exists():   # first-request size of each configuration (warm-up first)
        idle = {}
        mc.run_full(mc.build(mc.WORK / "m4", {}), "x", max_turns=1, timeout=180)
        for c in ("empty", "flat", "hub", "hubmanual"):
            wd = mc.build(mc.WORK / "m4", {}) if c == "empty" else build(c, suite)
            idle[c] = mc.run_full(wd, "x", max_turns=1, timeout=180)["first_request_total"]
        idle_f.write_text(json.dumps(idle, indent=1) + "\n", encoding="utf-8", newline="\n")
        print("idle", idle, flush=True)
    plan = [(c, "pos", t, i, rep) for c in ("flat", "hub") for t in P for i in range(4) for rep in (1, 2)]
    plan += [(c, "neg", "none", i, rep) for c in ("flat", "hub") for i in range(4) for rep in (1, 2)]
    plan += [("hubmanual", "pos", "changelog-entry", i, 1) for i in range(4)]
    random.Random(12).shuffle(plan)
    for config, kind, target, i, rep in plan:
        if (config, kind, target, i, rep) in done:
            continue
        wd = build(config, suite)
        prompt = P[target][i] if kind == "pos" else NEG[i]
        if kind == "neg":
            r = mc.first_move(wd, prompt)
            row = {"config": config, "kind": kind, "target": target, "prompt_id": i, "rep": rep, "decision": r["decision"], "called_any": r["decision"].startswith("skill:"), "rate_limit": r["rate_limit"]}
        else:
            r = mc.run_full(wd, prompt, max_turns=8, timeout=400, extra_args=ALLOW)
            tools = r["tools"]
            skill_calls = [((re.search(r'"skill":\s*"([^"]+)"', x[1]) or [None, x[1]])[1]) for x in tools if x[0] == "Skill"]
            reads = [x[1] for x in tools if x[0] == "Read"]
            if config == "flat":
                ok = target in skill_calls
            elif config == "hub":
                ok = "dev-workflows" in skill_calls and any(f"library/{target}" in x.replace("\\\\", "/") for x in reads)
            else:
                ok = target in skill_calls
            u = r["usage"]
            row = {"config": config, "kind": kind, "target": target, "prompt_id": i, "rep": rep, "ok": ok, "skill_calls": skill_calls, "reads": len(reads), "tool_calls": len(tools),
                   "output_tokens": u.get("output_tokens"), "input_total": (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0),
                   "answer_head": r["answer"][:160], "rate_limit": r["rate_limit"]}
        with raw.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row) + "\n")
        rl = r["rate_limit"]
        print(config, kind, target, i, rep, row.get("ok", row.get("decision")), rl and rl.get("five_hour"), flush=True)
        if rl and (rl.get("five_hour") or 0) >= a.stop_at:
            print("STOP: meter at the limit")
            return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
