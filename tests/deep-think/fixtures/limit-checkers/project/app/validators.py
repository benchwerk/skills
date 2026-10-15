def make_checkers(limits):
    """Return one function per limit; each tells whether a value is at most its limit."""
    checkers = []
    for limit in limits:
        checkers.append(lambda value: value <= limit)
    return checkers
