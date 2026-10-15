def _key(version):
    return tuple(int(part) for part in version.split("."))


def latest(versions):
    """versions are strings like '1.10.2'. Return the highest one."""
    return max(versions, key=_key)
