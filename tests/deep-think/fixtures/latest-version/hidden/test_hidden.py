from app.releases import sort_releases
from app.versions import latest


def test_primary_numeric_order():
    assert latest(["1.9.0", "1.10.0"]) == "1.10.0"
    assert latest(["2.0.0", "10.0.0", "9.9.9"]) == "10.0.0"


def test_second_sort_releases():
    releases = [{"version": "1.10.0"}, {"version": "1.2.0"}, {"version": "1.9.1"}]
    assert [r["version"] for r in sort_releases(releases)] == ["1.2.0", "1.9.1", "1.10.0"]


def test_regression_simple():
    assert latest(["1.0.0", "2.0.0"]) == "2.0.0"
