#!/usr/bin/env python3
"""skill_audit.py - checks Claude Code skills against what the benchwerk skill studies measured. Read-only; standard library only.

  python skill_audit.py <skills folder or a single skill folder> [--budget-tokens 9000]

Per skill it reports ERROR (the skill will not load or work), WARN (a measured risk) and INFO. For a folder of skills it also estimates the listing cost and how many
skills can keep their description (see the notes at the end of the output; every estimate is labelled). Exit code 1 if there is an ERROR.

Rules and where they come from (benchwerk skills study, Claude Code 2.1.286, Sonnet 5.5):
  - a SKILL.md without a frontmatter block is not loaded; the description is cut at about 1,536 characters
  - a description that names the situation in the user's words was called in 91.7% of runs, a broad "any non-trivial task" one in 0% (Part 18)
  - an instruction inside the description ("Always call this skill ...") was ignored in 24 of 24 runs (Part 18)
  - in a long list names are always shown, descriptions only while a budget lasts, in folder order; a descriptive name still got the skill called when its description was cut,
    an opaque name did not (M2b, M2c); manual-only skills are not listed and use no budget (M2d)
  - a skill that points at a file that does not exist is not noticed by Claude until it follows the pointer (Part 17, Amendment 2)
"""
import argparse
import math
import re
import sys
from pathlib import Path

CHARS_PER_TOKEN = 3.05      # calibrated on 15 suite skills: 1,165 listing tokens for 3,555 characters of name plus description (an estimate)
BODY_TOKENS_PER_CHAR = 0.4  # measured: 0.397 over the 20 most-installed skills
STOP = set("a an the and or of to in for on with is are be as at by it this that from use when user users asks ask not do does if its into any".split())
CMD = re.compile(r"\b(always|never|must|you should|make sure)\b[^.]{0,60}\b(call|use|invoke|load|run)\b[^.]{0,30}\b(this|the) skill\b", re.I)
REF = re.compile(r"(?<![\w.-])((?:scripts|references|assets|templates|examples|docs)/[\w./-]+\.\w+)")


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n?(.*)", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        k = re.match(r"([\w-]+):\s*(.*)", line)
        if k:
            fm[k.group(1)] = k.group(2).strip().strip("'\"")
    return fm, m.group(2)


def words(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}


def audit_skill(folder):
    out, info = [], {"folder": folder}
    f = folder / "SKILL.md"
    if not f.exists():
        return [("ERROR", "no SKILL.md in the folder")], info
    fm, body = parse(read(f))
    if fm is None:
        return [("ERROR", "no frontmatter block (--- ... ---): the skill is not loaded")], info
    name, desc = fm.get("name", ""), fm.get("description", "")
    manual = fm.get("disable-model-invocation", "").lower() == "true"
    info.update(name=name or folder.name, desc=desc, body_chars=len(body), manual=manual, desc_chars=len(desc))
    if not name:
        out.append(("WARN", "no name in the frontmatter (the folder name is used)"))
    elif name != folder.name:
        out.append(("INFO", f"name '{name}' differs from the folder '{folder.name}' (loads anyway)"))
    if name and not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
        out.append(("WARN", f"name '{name}' is not lower-case kebab-case of at most 64 characters"))
    if not desc:
        out.append(("ERROR", "no description: Claude has nothing to match a request against"))
    else:
        if len(desc) > 1536:
            out.append(("ERROR", f"description is {len(desc)} characters; it is cut at about 1,536"))
        elif len(desc) > 500:
            out.append(("WARN", f"description is {len(desc)} characters; long descriptions use the shared listing budget and fewer skills keep theirs (about 100 characters fit twice as many as 200)"))
        elif len(desc) < 40:
            out.append(("WARN", f"description is only {len(desc)} characters; it may not name the situation"))
        if not re.search(r"\buse (this )?(skill )?(when|whenever|before|after|at the start|if)\b|\bwhen the user\b|\bwhen you\b", desc, re.I):
            out.append(("WARN", "the description does not say when to use the skill ('Use when the user ...'): a topic-only or broad description was called in 0% of runs for a process skill"))
        if CMD.search(desc):
            out.append(("WARN", "the description contains an instruction to call the skill; such instructions were ignored in 24 of 24 runs. Describe the situation instead"))
        if re.search(r"\bany (non-?trivial )?(task|request|work)\b|\beverything\b|\bwhenever possible\b", desc, re.I):
            out.append(("WARN", "the description is broad ('any task'); a broad description was never picked, a situation was"))
        if not re.search(r"\b(do not|don't|not for|except)\b", desc, re.I) and len(desc) > 80:
            out.append(("INFO", "no 'Do not use for ...' sentence: a scope sentence helps keep near-misses out (not measured on its own)"))
        nw = words(name.replace("-", " "))
        if name and nw and not (nw & words(desc)) and not manual:
            out.append(("WARN", f"the name '{name}' shares no word with the description; when the description is cut from a long list only the name is seen, and an opaque name was called in 0% of runs"))
    for ref in sorted(set(REF.findall(body))):
        if not (folder / ref).exists():
            out.append(("ERROR", f"the body refers to '{ref}', which does not exist in the skill folder"))
    info["invoke_tokens"] = round(len(body) * BODY_TOKENS_PER_CHAR)
    if len(body) > 12000:
        out.append(("WARN", f"the body is {len(body)} characters (about {info['invoke_tokens']} tokens each time the skill runs); the median popular skill is about 8,000 characters"))
    if re.search(r"\.\.\.\s*$|\bTODO\b|\bFIXME\b", body, re.M):
        out.append(("INFO", "the body contains TODO, FIXME or an ellipsis at a line end"))
    if manual:
        out.append(("INFO", "manual-only: not listed for Claude, no listing cost, never picked automatically"))
    return out, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--budget-tokens", type=int, default=9000, help="assumed listing budget (an estimate from the 1M-window measurements)")
    a = ap.parse_args()
    root = Path(a.path)
    folders = [root] if (root / "SKILL.md").exists() else sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    if not folders:
        print("no skills found under", root)
        return 2
    errors = 0
    infos = []
    for fo in folders:
        res, info = audit_skill(fo)
        infos.append(info)
        print(f"== {fo.name}" + (" (manual-only)" if info.get("manual") else ""))
        for level, msg in res:
            print(f"  {level}: {msg}")
            errors += level == "ERROR"
        if not res:
            print("  ok")
    auto = [i for i in infos if i.get("desc") and not i.get("manual")]
    print(f"\n== collection: {len(infos)} skills, {len(auto)} automatic, {len(infos) - len(auto)} manual-only or unreadable")
    name_tok = lambda i: math.ceil(len(i["name"]) / CHARS_PER_TOKEN) + 2
    desc_tok = lambda i: math.ceil(i["desc_chars"] / CHARS_PER_TOKEN)
    total = sum(name_tok(i) + desc_tok(i) for i in auto)
    print(f"  estimated listing cost: about {total} tokens if every description is shown (estimate: {CHARS_PER_TOKEN} characters per token)")
    used = sum(name_tok(i) for i in auto)
    shown = 0
    for i in sorted(auto, key=lambda i: i["folder"].name):
        if used + desc_tok(i) <= a.budget_tokens:
            used += desc_tok(i)
            shown += 1
    print(f"  with a listing budget of about {a.budget_tokens} tokens (estimate), about {shown} of {len(auto)} automatic skills keep their description; the rest show only the name, in folder order")
    if shown < len(auto):
        print("  -> make rarely used skills manual-only, shorten descriptions (100 characters fit about twice as many as 200), and give every skill a name that says what it does")
    ws = [(i, words(i["desc"])) for i in auto]
    pairs = []
    for x in range(len(ws)):
        for y in range(x + 1, len(ws)):
            u = ws[x][1] | ws[y][1]
            j = len(ws[x][1] & ws[y][1]) / len(u) if u else 0
            if j >= 0.5:
                pairs.append((j, ws[x][0]["folder"].name, ws[y][0]["folder"].name))
    for j, p, q in sorted(pairs, reverse=True)[:10]:
        print(f"  INFO: '{p}' and '{q}' share {int(100 * j)}% of their description words (in the overlap test near-duplicates were still told apart by their content, 94.8% correct; only the right skill not being called was seen)")
    print("\nNotes: token figures are estimates; the budget figure was measured on Claude Code 2.1.286 with the 1M window and may differ on other versions and windows.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
