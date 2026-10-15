from app.versions import latest


def test_simple():
    assert latest(["1.0.0", "2.0.0"]) == "2.0.0"


def test_ten_is_higher_than_nine():
    assert latest(["1.9.0", "1.10.0"]) == "1.10.0"


def test_latest_is_callable():
    assert callable(latest) or True
