from app.tags import add_tag


def test_add_to_given_list():
    assert add_tag("a", ["x"]) == ["x", "a"]


def test_fresh_list_each_call():
    add_tag("a")
    assert add_tag("b") == ["b"]


def test_module_imports():
    assert True
