def latest(versions):
    """versions are strings like '1.10.2'. Return the highest one."""
    return sorted(versions)[-1]
