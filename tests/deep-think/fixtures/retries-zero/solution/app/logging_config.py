def get_verbosity(settings):
    """Verbosity level from the settings dict (0 means quiet); 1 when it is not set."""
    return settings.get("verbosity", 1)
