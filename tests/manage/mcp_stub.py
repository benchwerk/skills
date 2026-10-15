#!/usr/bin/env python3
"""A minimal MCP server over stdio with N tools, for measuring what tool definitions cost in the first request.   python mcp_stub.py <N>
The first 15 tools carry the descriptions of the 15 suite skills (so a tool and a skill describe the same thing); further tools are synthetic.
Every tool takes an `input` string and an optional `mode`. Calls return "ok". Standard library only."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manage_common as mc


def tools(n):
    suite = mc.suite_skills()
    descs = [(k.replace("-", "_"), v[0]) for k, v in suite.items()]
    syn = mc.synthetic(max(0, n - len(descs)), seed=31, prefix="t")
    descs += [(k.replace("-", "_"), v) for k, v in syn.items()]
    out = []
    for name, d in descs[:n]:
        out.append({"name": name[:60], "description": d,
                    "inputSchema": {"type": "object", "properties": {"input": {"type": "string", "description": "The text to work on."},
                                                                     "mode": {"type": "string", "enum": ["short", "full"], "description": "How much detail to return."}},
                                    "required": ["input"]}})
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    tl = tools(n)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            m = json.loads(line)
        except ValueError:
            continue
        mid, method = m.get("id"), m.get("method")
        if mid is None:
            continue   # a notification
        if method == "initialize":
            res = {"protocolVersion": (m.get("params") or {}).get("protocolVersion", "2024-11-05"), "capabilities": {"tools": {}}, "serverInfo": {"name": "stub", "version": "0.1"}}
        elif method == "tools/list":
            res = {"tools": tl}
        elif method == "tools/call":
            res = {"content": [{"type": "text", "text": "ok"}]}
        else:
            res = {}
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "result": res}) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
