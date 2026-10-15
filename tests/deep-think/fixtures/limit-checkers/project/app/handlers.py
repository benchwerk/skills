def make_greeters(names):
    """Return one function per name; each returns a greeting for that name."""
    greeters = []
    for name in names:
        greeters.append(lambda: "hello " + name)
    return greeters
