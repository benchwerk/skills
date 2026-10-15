from datetime import datetime, timezone


def seconds_left(expires_at):
    """Seconds until expires_at (an ISO 8601 string with an offset); negative when past."""
    return (datetime.fromisoformat(expires_at) - datetime.now(timezone.utc)).total_seconds()
