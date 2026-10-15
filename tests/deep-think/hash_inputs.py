#!/usr/bin/env python3
"""Writes inputs_hashes.json: the sha256 of every file the deep-think test depends on (fixtures, hidden tests, checkers, runner, candidate skills).
Committed together with prediction.md, so that none of them can change quietly after the predictions are written.   python hash_inputs.py [--check]"""
import hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


files = {}
for base, pattern in ((HERE / "fixtures", "**/*"), (REPO / "candidates", "**/*")):
    for p in sorted(base.glob(pattern)):
        if p.is_file() and "__pycache__" not in p.parts:
            files[p.relative_to(REPO).as_posix()] = sha(p)
for name in ("general_tasks.py", "score_run.py", "run_deepthink.py", "supervise_deepthink.py", "hash_inputs.py", "description_variants.py", "analyze_deepthink.py", "analyze_amend2.py", "rescore_general.py", "validate_fixtures.py", "build_fixtures.py", "prediction.md"):
    files[(HERE / name).relative_to(REPO).as_posix()] = sha(HERE / name)
out = HERE / (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "inputs_hashes.json")
if "--check" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    bad = [k for k in old if old[k] != files.get(k)] + [k for k in files if k not in old and k != "tests/deep-think/prediction.md"]
    print("unchanged" if not bad else "CHANGED: " + ", ".join(bad))
    sys.exit(1 if bad else 0)
out.write_text(json.dumps(files, indent=1) + "\n", encoding="utf-8", newline="\n")
print(len(files), "files hashed ->", out.name)
