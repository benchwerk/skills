import pytest

from app.attachments import attachment_path
from app.uploads import upload_path


@pytest.mark.parametrize("name", ["../secret", "../../etc/passwd", "/etc/passwd", "a/../../b", ".."])
def test_primary_names_that_escape_are_refused(name):
    with pytest.raises(ValueError):
        upload_path(name)


@pytest.mark.parametrize("folder,filename", [("../x", "a.txt"), ("ok", "../../a.txt"), ("/abs", "a.txt"), ("ok", "/etc/passwd")])
def test_second_attachment_names_that_escape_are_refused(folder, filename):
    with pytest.raises(ValueError):
        attachment_path(folder, filename)


def test_regression_good_names_still_work():
    assert upload_path("report.pdf") == "/srv/uploads/report.pdf"
    assert upload_path("a/b.txt") == "/srv/uploads/a/b.txt"
    assert attachment_path("inv", "1.pdf") == "/srv/attachments/inv/1.pdf"
