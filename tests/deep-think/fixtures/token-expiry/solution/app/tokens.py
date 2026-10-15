from datetime import datetime, timezone


def is_expired(expires_at):
    """expires_at is an ISO 8601 string with an offset, such as 2026-10-08T10:00:00+00:00."""
    return datetime.fromisoformat(expires_at) < datetime.now(timezone.utc)
