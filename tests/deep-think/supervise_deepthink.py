#!/usr/bin/env python3
"""Runs run_deepthink.py until every planned run has a row. When the runner stops because the five-hour meter reached its limit (exit code 3), waits until
the session meter is below 40% and starts it again. Keeps the computer awake while it works. Arguments are passed to the runner.
  CLAUDE_CONFIG_DIR=C:/Users/.../claude-bench CLAUDE_BIN=<pinned exe> python supervise_deepthink.py [runner arguments]"""
import ctypes, os, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001


def session_percent():
    p = subprocess.run([os.environ["CLAUDE_BIN"], "-p", "/usage"], capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=120)
    m = re.search(r"Current session:\s*(\d+)%", p.stdout)
    return int(m.group(1)) if m else None


def main():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    try:
        for attempt in range(1, 30):
            code = subprocess.run([sys.executable, str(HERE / "run_deepthink.py"), *sys.argv[1:]]).returncode
            print(f"[supervisor] attempt {attempt}: runner exit {code}", flush=True)
            if code == 0:
                return 0
            if code != 3:
                print("[supervisor] unexpected exit; stopping", flush=True)
                return code
            while True:
                time.sleep(300)
                pct = session_percent()
                print(f"[supervisor] waiting; session meter {pct}%", flush=True)
                if pct is not None and pct < 40:
                    break
    finally:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    return 1


if __name__ == "__main__":
    sys.exit(main())
