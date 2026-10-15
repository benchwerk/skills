"""Shared helpers for the skill-management tests (Part 16): building a working folder with a given set of skills, synthetic skills with realistic
descriptions, and calling Claude Code in print mode, either to the end (collect the answer) or only up to the first decision (skill called or not).
Standard library only. Needs CLAUDE_CONFIG_DIR (isolated, logged in, Windows path form) and CLAUDE_BIN (the pinned executable)."""
import json
import os
import random
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SUITE = REPO / "skills"
WORK = Path(os.environ.get("MG_WORK", r"C:\skillctx\mg"))
MODEL = "claude-sonnet-5-5[1m]"
EXTRA = ["--setting-sources", "project,local", "--strict-mcp-config", "--no-session-persistence"]

VERBS = ["review", "summarise", "rewrite", "audit", "plan", "draft", "check", "convert", "explain", "format", "compare", "estimate", "outline", "translate", "validate"]
OBJECTS = ["invoice", "contract", "recipe", "itinerary", "timesheet", "playlist", "budget", "lease", "newsletter", "resume", "syllabus", "workout", "garden layout",
           "menu", "press release", "grant proposal", "shift roster", "meal plan", "packing list", "inventory sheet", "survey", "lab report", "podcast outline",
           "wedding schedule", "tax checklist", "moving checklist", "bike repair", "birdwatching log", "chess opening", "crossword", "knitting pattern", "poem",
           "job posting", "customer email", "support ticket", "release checklist", "warehouse pick list", "board game rules", "travel visa form", "fund report"]
QUALIFIERS = ["with short sentences", "for a non-expert reader", "against a checklist", "and list open questions", "and keep a neutral tone", "with a risk table",
              "and note anything missing", "in plain language", "and suggest next steps", "with examples"]


def env():
    e = {k: v for k, v in os.environ.items() if not (k.upper().startswith(("ANTHROPIC_", "CLAUDE_CODE_")) or k.upper() == "CLAUDECODE")}
    e["CLAUDE_CONFIG_DIR"] = os.environ["CLAUDE_CONFIG_DIR"]
    return e


def exe():
    return os.environ["CLAUDE_BIN"]


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


def skill_text(name, description, body="Synthetic placeholder, never invoked.", manual=False):
    fm = f"---\nname: {name}\ndescription: {description}\n"
    if manual:
        fm += "disable-model-invocation: true\n"
    return fm + f"---\n\n# {name}\n\n{body}\n"


def synthetic(n, seed, min_len=110, max_len=420, prefix="x"):
    """n unique skills with plausible descriptions of varied length: {name: description}. Deterministic for a seed."""
    rnd = random.Random(seed)
    out = {}
    pairs = [(v, o) for v in VERBS for o in OBJECTS]
    rnd.shuffle(pairs)
    for i, (v, o) in enumerate(pairs[:n]):
        name = f"{prefix}{i:03d}-" + (v + "-" + o).replace(" ", "-")
        target = rnd.randint(min_len, max_len)
        d = f"Use when the user asks to {v} a {o}. "
        while len(d) < target:
            d += rnd.choice([f"Covers the usual steps for a {o}, {rnd.choice(QUALIFIERS)}. ", f"Do not use for unrelated documents. ", f"Gives a short report at the end. ",
                             f"Asks for missing details only when they change the result. ", f"Works from the text the user pastes. "])
        out[name] = d.strip()[:target].rstrip()
    return out


def build(run_dir, skills, files=None, manual=()):
    """skills: {name: (description, body) or description}. A fresh project folder at run_dir/project."""
    wd = run_dir / "project"
    if wd.exists():
        rm_tree(wd)
    (wd / ".claude" / "skills").mkdir(parents=True)
    for name, v in skills.items():
        desc, body = (v, "Synthetic placeholder, never invoked.") if isinstance(v, str) else v
        d = wd / ".claude" / "skills" / name
        d.mkdir()
        (d / "SKILL.md").write_text(skill_text(name, desc, body, manual=name in manual), encoding="utf-8", newline="\n")
    for rel, text in (files or {}).items():
        p = wd / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
    return wd


def suite_skills(names=None):
    """the real suite skills: {name: (description, body)}"""
    out = {}
    for d in sorted(SUITE.iterdir()):
        if names is not None and d.name not in names:
            continue
        t = (d / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
        desc = re.search(r"^description: (.*)$", m.group(1), re.M).group(1)
        out[d.name] = (desc, m.group(2).strip())
    return out


def rate_limit(line):
    try:
        i = json.loads(line)["rate_limit_info"]
        w = i.get("unifiedWindows", {})
        return {"status": i.get("status"), "five_hour": w.get("five_hour", {}).get("utilization"), "seven_day": w.get("seven_day", {}).get("utilization")}
    except (ValueError, KeyError):
        return None


def run_full(wd, prompt, max_turns=2, timeout=300, extra_args=()):
    """run to the end; returns {answer, usage, rate_limit, first_request_total, seconds}"""
    cmd = [exe(), "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns), "--model", MODEL, *EXTRA, *extra_args]
    p = subprocess.Popen(cmd, cwd=wd, env=env(), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    timer = threading.Timer(timeout, kill_tree, [p])
    timer.start()
    t0 = time.time()
    answer, usage, rl, first_total, tools, init_skills, models = "", {}, None, None, [], [], []
    try:
        for line in p.stdout:
            if not line.startswith("{"):
                continue
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "rate_limit_event" and rl is None:
                rl = rate_limit(line)
            if e.get("type") == "system" and e.get("subtype") == "init":
                init_skills = e.get("skills", [])
            if e.get("type") == "assistant":
                models.append((e.get("message") or {}).get("model"))
                u = (e.get("message") or {}).get("usage") or {}
                if first_total is None:
                    first_total = sum(u.get(k, 0) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
                for c in (e.get("message") or {}).get("content", []) or []:
                    if c.get("type") == "tool_use":
                        tools.append((c.get("name"), json.dumps(c.get("input"))[:200]))
            if e.get("type") == "result":
                answer, usage = e.get("result") or "", e.get("usage") or {}
    finally:
        timer.cancel()
        kill_tree(p)
    return {"answer": answer, "usage": usage, "rate_limit": rl, "first_request_total": first_total, "tools": tools, "init_skills": init_skills, "models": models, "seconds": round(time.time() - t0, 1)}


def first_move(wd, prompt, timeout=150):
    """watch the stream until the model's first decision: a Skill call (with the skill name), a long text answer, or the end. Nothing after the decision is generated."""
    cmd = [exe(), "-p", prompt, "--output-format", "stream-json", "--verbose", "--include-partial-messages", "--max-turns", "3", "--model", MODEL, *EXTRA]
    p = subprocess.Popen(cmd, cwd=wd, env=env(), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    timer = threading.Timer(timeout, kill_tree, [p])
    timer.start()
    t0, decision, rl, buf, tool, text, others, usage1 = time.time(), None, None, "", None, 0, [], None
    try:
        for line in p.stdout:
            if not line.startswith("{"):
                continue
            try:
                e = json.loads(line)
            except ValueError:
                continue
            t = e.get("type")
            if t == "rate_limit_event" and rl is None:
                rl = rate_limit(line)
            if t == "result":
                break
            if t != "stream_event":
                continue
            ev = e["event"]
            et = ev.get("type")
            if et == "message_start" and usage1 is None:
                usage1 = (ev.get("message") or {}).get("usage")
            if et == "content_block_start":
                cb = ev["content_block"]
                tool = cb.get("name") if cb["type"] == "tool_use" else None
                if tool and tool != "Skill":
                    others.append(tool)
                buf = ""
            elif et == "content_block_delta":
                d = ev["delta"]
                if d.get("type") == "text_delta":
                    text += len(d["text"])
                    if text > 600:
                        decision = "text"
                        break
                elif d.get("type") == "input_json_delta" and tool == "Skill":
                    buf += d.get("partial_json", "")
                    try:
                        decision = "skill:" + json.loads(buf).get("skill", "?")
                        break
                    except ValueError:
                        pass
    finally:
        timer.cancel()
        kill_tree(p)
    if decision is None:
        decision = "text" if text else ("none" if time.time() - t0 < timeout - 1 else "timeout")
    return {"decision": decision, "other_tools": others, "rate_limit": rl, "seconds": round(time.time() - t0, 1), "first_request_usage": usage1}
