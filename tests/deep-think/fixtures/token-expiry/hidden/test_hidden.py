from app.sessions import seconds_left
from app.tokens import is_expired


def test_primary_expired_with_offsets():
    assert is_expired("2000-01-01T00:00:00+00:00") is True
    assert is_expired("2000-01-01T00:00:00+02:00") is True
    assert is_expired("2099-01-01T00:00:00+05:30") is False


def test_second_seconds_left():
    assert seconds_left("2099-01-01T00:00:00+00:00") > 0
    assert seconds_left("2000-01-01T00:00:00+00:00") < 0


def test_second_far_future_is_big():
    assert seconds_left("2099-01-01T00:00:00+00:00") > 10**9
