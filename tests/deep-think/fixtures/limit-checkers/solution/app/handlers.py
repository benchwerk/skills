def make_greeters(names):
    """Return one function per name; each returns a greeting for that name."""
    return [(lambda name=name: "hello " + name) for name in names]
