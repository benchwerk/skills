#!/usr/bin/env python3
"""MCP tools against skills: first-request size with N MCP tools (stub server) and with the same descriptions as skills.   python m_mcp.py -> results/mcp/raw.jsonl"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_common as mc

OUT = mc.HERE / "results" / "mcp"
STUB = str(mc.HERE / "mcp_stub.py")


def init_tools(wd, extra):
    """names of tools and MCP servers reported at the start of a session"""
    cmd = [mc.exe(), "-p", "x", "--output-format", "stream-json", "--verbose", "--max-turns", "1", "--model", mc.MODEL, *mc.EXTRA, *extra]
    p = subprocess.run(cmd, cwd=wd, env=mc.env(), stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
    for line in p.stdout.splitlines():
        if line.startswith("{") and '"subtype":"init"' in line.replace(" ", ""):
            e = json.loads(line)
            return e.get("tools", []), e.get("mcp_servers", [])
    return [], []


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    suite = mc.suite_skills()
    for label, n, kind in (("empty", 0, None), ("mcp5", 5, "mcp"), ("mcp15", 15, "mcp"), ("mcp40", 40, "mcp"), ("skills15", 15, "skills")):
        wd = mc.build(mc.WORK / "mcp", suite if kind == "skills" else {})
        extra = []
        if kind == "mcp":
            cfg = wd.parent / "mcp.json"
            cfg.write_text(json.dumps({"mcpServers": {"stub": {"command": sys.executable, "args": [STUB, str(n)]}}}), encoding="utf-8")
            extra = ["--mcp-config", str(cfg)]
        if not rows:
            mc.run_full(wd, "x", max_turns=1, timeout=180, extra_args=extra)   # warm-up
        a = mc.run_full(wd, "x", max_turns=1, timeout=180, extra_args=extra)
        b = mc.run_full(wd, "x", max_turns=1, timeout=180, extra_args=extra)
        tools, servers = init_tools(wd, extra)
        row = {"label": label, "n": n, "kind": kind, "first_request": b["first_request_total"], "repeat_equal": a["first_request_total"] == b["first_request_total"],
               "tools_at_start": len(tools), "mcp_tools_at_start": sum(1 for t in tools if str(t).startswith("mcp__")), "servers": servers}
        rows.append(row)
        print(row, flush=True)
    base = rows[0]["first_request"]
    for r in rows:
        r["added"] = r["first_request"] - base
    (OUT / "raw.json").write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8", newline="\n")
    for r in rows:
        print(f"{r['label']:9s} first request {r['first_request']:6d}  added {r['added']:6d}  per item {r['added'] / r['n'] if r['n'] else 0:6.1f}  mcp tools at start {r['mcp_tools_at_start']}")


if __name__ == "__main__":
    main()
