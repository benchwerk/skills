from app.markup import bold_text


def test_single_bold():
    assert bold_text("<b>a</b>") == "a"


def test_two_bold_elements():
    assert bold_text("<b>a</b> and <b>b</b>") == "a"


def test_no_bold():
    assert bold_text("plain") is None
