def make_checkers(limits):
    """Return one function per limit; each tells whether a value is at most its limit."""
    return [(lambda value, limit=limit: value <= limit) for limit in limits]
