from app.handlers import make_greeters
from app.validators import make_checkers


def test_primary_each_checker_has_its_own_limit():
    c = make_checkers([1, 10, 100])
    assert [f(5) for f in c] == [False, True, True]
    assert [f(50) for f in c] == [False, False, True]


def test_second_each_greeter_has_its_own_name():
    g = make_greeters(["ann", "bo"])
    assert [f() for f in g] == ["hello ann", "hello bo"]


def test_regression_empty_lists():
    assert make_checkers([]) == [] and make_greeters([]) == []
