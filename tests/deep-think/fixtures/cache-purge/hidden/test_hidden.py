from app.cache import drop_expired
from app.registry import remove_empty


def test_primary_expired_removed():
    assert drop_expired({"a": 1, "b": 10, "c": 5}, 5) == {"b": 10}


def test_primary_same_object_returned():
    cache = {"a": 1}
    assert drop_expired(cache, 5) is cache and cache == {}


def test_second_empty_groups_removed():
    assert remove_empty({"x": [], "y": [1], "z": []}) == {"y": [1]}


def test_regression_nothing_to_remove():
    assert drop_expired({"a": 10}, 5) == {"a": 10}
    assert remove_empty({"y": [1]}) == {"y": [1]}
