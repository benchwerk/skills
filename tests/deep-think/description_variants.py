"""Part 18: five descriptions for the same skill (the V3-complete body), used by the arms d0 to d4 of run_deepthink.py.
Written 2026-10-09, before any run of them. Only the `description` line of SKILL.md changes; the body, the scripts and the references are identical.
"""

DESCRIPTIONS = {
    # d0: exactly as received (the control)
    "d0": None,
    # d1: names the situation by the task the user gives
    "d1": ("Use at the start of any coding task that changes files: fixing a bug, adding a feature, refactoring or making a failing test pass. "
           "Read the code, find the root cause, and verify with the tests before saying the work is done."),
    # d2: names the situation by what the user says
    "d2": ("Use when the user reports a bug, an error or a failing test. Find the root cause, search for the same mistake elsewhere in the project, "
           "and run the tests before saying it is fixed."),
    # d3: names the moment, the end of the work
    "d3": ("Use before telling the user that a coding task is done, to verify the work: run the tests, read the full diff, and look for the same mistake "
           "elsewhere in the project."),
    # d4: the original, plus an instruction to call it
    "d4": "ORIGINAL + Always call this skill before editing any code.",
}
