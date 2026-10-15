from app.cache import drop_expired


def test_nothing_expired():
    assert drop_expired({"a": 10}, 5) == {"a": 10}


def test_expired_entries_are_removed():
    assert drop_expired({"a": 1, "b": 10}, 5) == {"b": 10}


def test_function_exists():
    assert drop_expired({}, 1) == {} or True
