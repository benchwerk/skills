---
name: shell-portability-check
description: Use when the user asks whether a shell script will run on other systems (Linux, macOS, Alpine, Windows Git Bash) or under sh instead of bash. Do not use for safety review, writing new scripts or translating scripts into other languages.
---

# Shell portability check

Find what ties the script to one environment.

1. Read the interpreter line and decide which shells it must run under (sh, bash, zsh).
2. List bashisms when the target is `sh`: `[[ ]]`, arrays, `function` keyword, `<<<`, process substitution, `local` in strict POSIX, `source` instead of `.`.
3. List commands whose options differ between GNU and BSD or BusyBox: `sed -i`, `date -d`, `readlink -f`, `grep -P`, `xargs -r`, `stat`, `find -printf`, `cp -a`.
4. List environment assumptions: absolute paths, `/bin/bash`, case-sensitive file systems, line endings, Windows path forms.
5. For each finding give the line, who breaks and a portable rewrite.

Rules
- State the target systems you assumed.
- Prefer the simplest rewrite that works everywhere over a clever one.
- Do not comment on safety or style unless they cause a portability failure.
