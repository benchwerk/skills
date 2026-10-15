from app.tokens import is_expired


def test_past_token_is_expired():
    assert is_expired("2000-01-01T00:00:00+00:00") is True


def test_future_token_is_not_expired():
    assert is_expired("2099-01-01T00:00:00+00:00") is False
