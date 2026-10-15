#!/usr/bin/env python3
"""Runner for the deep-think test (Part 17): coding fixtures and general tasks under several arms.

Arms (what the model is given besides the task):
  none          nothing
  sentence      CLAUDE.md with one line: "Be thorough: read before you edit, and verify your work before you say it is done."
  v2            candidates/deep-think-v2 installed as the skill `deep-think`, exactly as received
  v3            candidates/deep-think-v3, exactly as received (it refers to a script and a file that do not exist)
  v3c           candidates/deep-think-v3-complete (with scripts/check_work.py and references/lenses.md)
  placebo       the V3 name and description over a body of neutral text of the same length
  v3c-forced    like v3c, but the prompt starts with /deep-think (separates "did not trigger" from "did not help")

Every arm gets the same task text, the same fresh working folder (a git repository with one commit, so that check_work.py can diff), Sonnet 5.5,
the pinned Claude Code executable and an isolated config. Coding tasks run with edits accepted and a fixed list of allowed shell commands.
Rows are appended to results/<date>_<machine>_deepthink/raw.jsonl; finished runs are skipped on a restart. The runner stops at --stop-at of the
five-hour meter (default 0.90) and says when to continue.

  CLAUDE_CONFIG_DIR=<isolated dir> CLAUDE_BIN=<pinned exe> python run_deepthink.py --dry-run
  ... python run_deepthink.py --arms none,v3c --tasks paging-first-page,offsite-a --reps 1 --stop-at 0.90
"""
import argparse
import datetime
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CAND = REPO / "candidates"
FIX = HERE / "fixtures"
WORK = Path(os.environ.get("DT_WORK", r"C:\skillctx\dt"))
MODEL = "claude-sonnet-5-5[1m]"
SEED = 20261008
STAMP = datetime.datetime.now().strftime("%m%d%H%M%S")
SENTENCE = "Be thorough: read before you edit, and verify your work before you say it is done."
ARMS = ["none", "sentence", "v2", "v3", "v3c", "placebo", "v3c-forced"]
EXTRA_ARMS = ["v2-forced", "v3-forced"]   # amendment 2, 2026-10-09
DESC = ["d0", "d1", "d2", "d3", "d4"]   # part 18, see description_variants.py
ALLOWED = ("Read,Glob,Grep,Edit,Write,Skill,Bash(python *),Bash(python3 *),Bash(pytest *),Bash(git *),Bash(grep *),Bash(find *),Bash(ls *),"
           "Bash(cat *),Bash(head *),Bash(tail *),Bash(wc *),Bash(sed *),Bash(pwd),Bash(cd *),Bash(echo *),Bash(mkdir *),Bash(diff *)")
EXTRA = ["--setting-sources", "project,local", "--strict-mcp-config", "--no-session-persistence"]
NEUTRAL = ("The kiln shed stands behind the old pottery. Clay is delivered on Mondays and stored under damp cloth. Glazes are mixed in small batches and labelled "
           "with the date. The studio keeps a notebook of firing temperatures, one page for each firing. Visitors are welcome on Saturdays, and the shop opens at ten. "
           "Tea is served in the garden when the weather allows. ")

sys.path.insert(0, str(HERE))
import general_tasks as G  # noqa: E402
from description_variants import DESCRIPTIONS  # noqa: E402


def env():
    e = {k: v for k, v in os.environ.items() if not (k.upper().startswith(("ANTHROPIC_", "CLAUDE_CODE_")) or k.upper() == "CLAUDECODE")}
    e["CLAUDE_CONFIG_DIR"] = os.environ["CLAUDE_CONFIG_DIR"]
    return e


def kill_tree(p):
    try:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True, timeout=30)
    except Exception:
        pass
    try:
        p.kill()
    except Exception:
        pass


def rm_tree(path):
    for _ in range(10):
        try:
            shutil.rmtree(path)
            return
        except FileNotFoundError:
            return
        except OSError:
            time.sleep(3)
    shutil.rmtree(path, ignore_errors=True)


def placebo_skill():
    v3 = (CAND / "deep-think-v3" / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"(---\n.*?\n---\n)(.*)", v3, re.S)
    n = len(m.group(2))
    body = "# Deep Think\n\n" + (NEUTRAL * (n // len(NEUTRAL) + 1))
    return m.group(1) + "\n" + body[: n - 1] + "\n"


def tasks():
    out = []
    for d in sorted(p for p in FIX.iterdir() if p.is_dir()):
        text = (d / "task.txt").read_text(encoding="utf-8").strip()
        out.append({"id": d.name, "fixture": d.name, "kind": "coding", "prompt": text})
        # amendment 1 (2026-10-08, before any scored run): the same task with "Please be thorough." appended, in five arms
        out.append({"id": d.name + "+thorough", "fixture": d.name, "kind": "coding", "prompt": text + " Please be thorough.",
                    "arms": {"none", "v2", "v3", "v3c", "placebo"}})
    for t in G.TASKS:
        out.append({"id": t["id"], "kind": "general", "prompt": t["prompt"].strip(), "family": t["family"]})
    return out


def build(arm, task, run_dir):
    wd = run_dir / "project"
    if wd.exists():
        rm_tree(wd)
    if task["kind"] == "coding":
        shutil.copytree(FIX / task["fixture"] / "project", wd)
    else:
        wd.mkdir(parents=True)
    if arm == "sentence":
        (wd / "CLAUDE.md").write_text(SENTENCE + "\n", encoding="utf-8", newline="\n")
    elif arm in DESC:   # part 18: the V3-complete skill with a different description line
        dest = wd / ".claude" / "skills" / "deep-think"
        shutil.copytree(CAND / "deep-think-v3-complete", dest)
        new = DESCRIPTIONS[arm]
        if new:
            f = dest / "SKILL.md"
            text = f.read_text(encoding="utf-8")
            old = re.search(r"^description: (.*)$", text, re.M).group(1)
            line = old + " Always call this skill before editing any code." if new.startswith("ORIGINAL") else new
            f.write_text(text.replace("description: " + old, "description: " + line, 1), encoding="utf-8", newline="\n")
    elif arm in ("v2", "v3", "v3c", "placebo", "v3c-forced", "v2-forced", "v3-forced"):
        dest = wd / ".claude" / "skills" / "deep-think"
        if arm == "placebo":
            dest.mkdir(parents=True)
            (dest / "SKILL.md").write_text(placebo_skill(), encoding="utf-8", newline="\n")
        else:
            src = CAND / {"v2": "deep-think-v2", "v3": "deep-think-v3", "v3c": "deep-think-v3-complete", "v3c-forced": "deep-think-v3-complete", "v2-forced": "deep-think-v2", "v3-forced": "deep-think-v3"}[arm]
            shutil.copytree(src, dest)
    if task["kind"] == "coding":
        for cmd in (["git", "init", "-q"], ["git", "config", "user.name", "dt"], ["git", "config", "user.email", "dt@example.invalid"], ["git", "config", "core.autocrlf", "false"],
                    ["git", "add", "-A"], ["git", "commit", "-q", "-m", "baseline"]):
            subprocess.run(cmd, cwd=wd, capture_output=True, timeout=60)
    return wd


def call(exe, wd, prompt, out_file, timeout, max_turns):
    cmd = [exe, "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns), "--model", MODEL,
           "--permission-mode", "acceptEdits", "--allowedTools", ALLOWED, *EXTRA]
    with open(out_file, "w", encoding="utf-8", newline="\n") as f:
        p = subprocess.Popen(cmd, cwd=wd, env=env(), stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.DEVNULL)
        timer = threading.Timer(timeout, kill_tree, [p])
        timer.start()
        t0 = time.time()
        try:
            p.wait()
        finally:
            timer.cancel()
            kill_tree(p)
    return round(time.time() - t0, 1), p.returncode


def read_stream(path):
    final, usage, turns, status, rl, skill_calls, tools = "", {}, None, None, None, [], []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("{"):
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "rate_limit_event" and rl is None:
            try:
                w = e["rate_limit_info"].get("unifiedWindows", {})
                rl = {"status": e["rate_limit_info"].get("status"), "five_hour": w.get("five_hour", {}).get("utilization"), "seven_day": w.get("seven_day", {}).get("utilization")}
            except (KeyError, AttributeError):
                pass
        if e.get("type") == "assistant":
            for c in (e.get("message") or {}).get("content", []) or []:
                if c.get("type") == "tool_use":
                    tools.append(c.get("name"))
                    if c.get("name") == "Skill":
                        skill_calls.append((c.get("input") or {}).get("skill"))
        if e.get("type") == "result":
            final, usage, turns, status = e.get("result") or "", e.get("usage") or {}, e.get("num_turns"), e.get("subtype")
    return {"final": final, "usage": usage, "turns": turns, "status": status, "rate_limit": rl, "skill_calls": skill_calls, "n_tools": len(tools)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--tasks", default="")
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--stop-at", type=float, default=0.90)
    ap.add_argument("--max-runs", type=int, default=0)
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--out", default="")
    ap.add_argument("--style", default="both", choices=["both", "plain", "thorough"])
    ap.add_argument("--kinds", default="coding,general")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    arms = a.arms.split(",")
    allt = tasks()
    want = set(a.tasks.split(",")) if a.tasks else None
    if a.style == "plain":
        allt = [t for t in allt if not t["id"].endswith("+thorough")]
    elif a.style == "thorough":
        allt = [t for t in allt if t["kind"] == "coding" and t["id"].endswith("+thorough")]
    pool = [t for t in allt if (not want or t["id"] in want) and t["kind"] in a.kinds.split(",")]
    plan = [{"task": t, "arm": arm, "rep": r} for t in pool for arm in arms for r in range(1, a.reps + 1) if not t.get("arms") or arm in t["arms"]]
    random.Random(SEED).shuffle(plan)
    out = Path(a.out) if a.out else HERE / "results" / f"{datetime.date.today()}_x86-laptop_deepthink"
    out.mkdir(parents=True, exist_ok=True)
    raw = out / "raw.jsonl"
    done = {(r["task"], r["arm"], r["rep"]) for r in map(json.loads, raw.read_text(encoding="utf-8").splitlines())} if raw.exists() else set()
    print(f"{len(plan)} runs planned, {len(done)} rows exist -> {out}")
    exe = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    n = 0
    for p in plan:
        t, arm, rep = p["task"], p["arm"], p["rep"]
        if (t["id"], arm, rep) in done:
            continue
        if a.max_runs and n >= a.max_runs:
            print("STOP: --max-runs reached")
            return 3
        run_dir = WORK / f"{STAMP}__{t['id']}__{arm}__{rep}"   # a new folder for every invocation: a folder held open by a lingering process cannot block a run
        run_dir.mkdir(parents=True, exist_ok=True)
        wd = build(arm, t, run_dir)
        prompt = ("/deep-think " if arm.endswith("-forced") else "") + t["prompt"]
        if a.dry_run:
            print(f"[dry] {t['id']} {arm} rep{rep}: {len(prompt)} chars, folder {wd}")
            n += 1
            if n >= 3:
                return 0
            continue
        secs, rc = call(exe, wd, prompt, run_dir / "stdout.jsonl", a.timeout, a.max_turns)
        s = read_stream(run_dir / "stdout.jsonl")
        row = {"task": t["id"], "kind": t["kind"], "arm": arm, "rep": rep, "seconds": secs, "exit": rc, "status": s["status"], "turns": s["turns"],
               "output_tokens": s["usage"].get("output_tokens"), "input_tokens": s["usage"].get("input_tokens"), "cache_creation": s["usage"].get("cache_creation_input_tokens"),
               "cache_read": s["usage"].get("cache_read_input_tokens"), "tool_calls": s["n_tools"], "skill_calls": s["skill_calls"],
               "triggered": "deep-think" in s["skill_calls"], "rate_limit": s["rate_limit"], "final_chars": len(s["final"])}
        if t["kind"] == "coding":
            sc = subprocess.run([sys.executable, str(HERE / "score_run.py"), t["fixture"], str(run_dir)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
            try:
                row["score"] = json.loads(sc.stdout)
            except ValueError:
                row["score"] = {"error": (sc.stderr or sc.stdout)[-300:]}
        else:
            chk = next(x for x in G.TASKS if x["id"] == t["id"])["check"]
            row["score"] = chk(s["final"])
            row["words"] = G.words(s["final"])
            (run_dir / "answer.txt").write_text(s["final"], encoding="utf-8", newline="\n")
        with raw.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row) + "\n")
        n += 1
        rl = s["rate_limit"]
        print(f"{t['id']:20s} {arm:11s} rep{rep} turns={s['turns']} out={row['output_tokens']} triggered={row['triggered']} meter={rl and rl.get('five_hour')}", flush=True)
        if s["status"] is None:
            print("STOP: no result from the model (a limit or an error); not spending more.")
            return 3
        if rl and ((rl.get("five_hour") or 0) >= a.stop_at or rl.get("status") not in (None, "allowed", "allowed_warning")):
            print(f"STOP: five-hour meter {rl.get('five_hour')} (status {rl.get('status')}); continue after the reset by running the same command.")
            return 3
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
