import posixpath

UPLOAD_DIR = "/srv/uploads"


def upload_path(name):
    """Where an uploaded file with this name is stored."""
    path = posixpath.normpath(posixpath.join(UPLOAD_DIR, name))
    if path != UPLOAD_DIR and not path.startswith(UPLOAD_DIR + "/"):
        raise ValueError("name leaves the upload folder")
    if path == UPLOAD_DIR or not name or posixpath.isabs(name):
        raise ValueError("invalid name")
    return path
