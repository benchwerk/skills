def drop_expired(cache, now):
    """cache maps key -> expiry time. Remove entries whose expiry is at or before now; return the cache."""
    for key in cache:
        if cache[key] <= now:
            del cache[key]
    return cache
