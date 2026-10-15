from app.errors import collect_error
from app.tags import add_tag


def test_primary_fresh_list_each_call():
    add_tag("a")
    add_tag("b")
    assert add_tag("c") == ["c"]


def test_second_errors_fresh_each_call():
    collect_error("one")
    collect_error("two")
    assert collect_error("three") == ["three"]


def test_regression_given_list_is_extended_and_returned():
    given = ["x"]
    result = add_tag("a", given)
    assert result == ["x", "a"] and result is given


def test_regression_errors_given_list():
    given = ["x"]
    assert collect_error("a", given) == ["x", "a"]
