def sort_releases(releases):
    """releases are dicts with a 'version' string like '1.10.2'. Return them from lowest to highest version."""
    return sorted(releases, key=lambda release: tuple(int(p) for p in release["version"].split(".")))
