---
name: bash-script-safety-review
description: Use when the user asks whether a Bash or shell script is safe to run, or to review it for dangerous mistakes, quoting problems and missing error handling. Do not use for writing new scripts, converting between shells or scheduling jobs.
---

# Bash script safety review

Read the whole script and report what could do damage.

1. Check the top of the file: interpreter line, `set -euo pipefail` (or a reason for not using it).
2. Check every destructive command (`rm`, `mv`, `dd`, `chmod`, `chown`, `>` redirects over files) for variables that can be empty or contain spaces. `rm -rf "$DIR/"` with an empty `DIR` is the classic case.
3. Check quoting: unquoted `$var` and `$(...)`, word splitting, globbing in loops.
4. Check `cd` without `|| exit`, reliance on the current directory, parsing of `ls` output, `eval`, `curl | sh`, use of `sudo`, hard-coded secrets.
5. Check temporary files (`mktemp`, cleanup with `trap`) and what happens if the script stops halfway.
6. For each finding give the line, the risk and the corrected line.

Rules
- Do not run the script.
- Rank findings: can lose data, can break things, style.
- End with a verdict: safe, safe after fixes, or do not run.
