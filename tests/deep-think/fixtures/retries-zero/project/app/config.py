def get_retries(settings):
    """Number of retries from the settings dict; 3 when it is not set."""
    return settings.get("retries") or 3
