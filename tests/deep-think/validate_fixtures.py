#!/usr/bin/env python3
"""Proves every fixture is sound before any model sees it. For each fixture, in temporary copies:

  A. the project as the model gets it: at least one visible test fails (the symptom) and the can't-fail test, if any, passes;
  B. project + hidden tests: every test_primary_* and every test_second_* test fails, every test_regression_* test passes;
  C. project + solution + hidden tests: everything passes;
  D. project + solution, visible tests only: everything passes.

  python validate_fixtures.py [fixture-id ...]       exit code 0 only if every check holds
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIX = Path(__file__).resolve().parent / "fixtures"


def pytest(cwd):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rA", "--tb=no", "-p", "no:cacheprovider", "--no-header"], cwd=cwd,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    res = {}
    for line in p.stdout.splitlines():
        m = re.match(r"(PASSED|FAILED|ERROR) (\S+)", line)
        if m:
            res[m.group(2)] = m.group(1)
    return res


def short(name):
    return name.split("::", 1)[-1]


def main():
    ids = sys.argv[1:] or sorted(p.name for p in FIX.iterdir() if p.is_dir())
    bad = 0
    for fid in ids:
        d = FIX / fid
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        problems = []
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "p"
            shutil.copytree(d / "project", base)
            a = pytest(base)
            failing = [k for k, v in a.items() if v != "PASSED"]
            if not failing:
                problems.append("A: no visible test fails")
            cf = meta.get("cannot_fail")
            if cf and a.get(cf) != "PASSED":
                problems.append(f"A: the can't-fail test does not pass: {cf}")
            shutil.copy(d / "hidden" / "test_hidden.py", base / "tests" / "test_hidden.py")
            b = pytest(base)
            for k, v in b.items():
                if "test_hidden.py" not in k:
                    continue
                s = short(k)
                if s.startswith(("test_primary", "test_second")) and v == "PASSED":
                    problems.append(f"B: should fail before the fix: {s}")
                if s.startswith(("test_regression",)) and v != "PASSED":
                    problems.append(f"B: should pass before the fix: {s}")
            if not any(short(k).startswith("test_primary") for k in b) or not any(short(k).startswith("test_second") for k in b):
                problems.append("B: missing primary or second tests")
            (base / "tests" / "test_hidden.py").unlink()
            for f in (d / "solution").rglob("*"):
                if f.is_file():
                    dest = base / f.relative_to(d / "solution")
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(f, dest)
            dres = pytest(base)
            if not dres or any(v != "PASSED" for v in dres.values()):
                problems.append("D: visible tests do not all pass with the solution: " + str({short(k): v for k, v in dres.items() if v != "PASSED"}))
            shutil.copy(d / "hidden" / "test_hidden.py", base / "tests" / "test_hidden.py")
            c = pytest(base)
            if not c or any(v != "PASSED" for v in c.values()):
                problems.append("C: not everything passes with the solution: " + str({short(k): v for k, v in c.items() if v != "PASSED"}))
        status = "OK " if not problems else "BAD"
        print(f"{status} {fid:18s} visible failing: {[short(x) for x in failing]}")
        for p in problems:
            print("     ", p)
        bad += bool(problems)
    print(f"{len(ids) - bad} of {len(ids)} fixtures sound")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
