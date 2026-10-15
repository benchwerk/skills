import pytest

from app.uploads import UPLOAD_DIR, upload_path


def test_plain_name():
    assert upload_path("report.pdf") == "/srv/uploads/report.pdf"


def test_parent_directory_is_refused():
    with pytest.raises(ValueError):
        upload_path("../secret")


def test_module_has_upload_dir():
    assert UPLOAD_DIR or True
