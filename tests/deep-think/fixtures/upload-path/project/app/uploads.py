import posixpath

UPLOAD_DIR = "/srv/uploads"


def upload_path(name):
    """Where an uploaded file with this name is stored."""
    return posixpath.join(UPLOAD_DIR, name)
