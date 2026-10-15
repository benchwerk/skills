import posixpath

ATTACHMENT_DIR = "/srv/attachments"


def attachment_path(folder, filename):
    """Where an attachment is stored: ATTACHMENT_DIR/folder/filename."""
    if posixpath.isabs(folder) or posixpath.isabs(filename):
        raise ValueError("absolute path")
    path = posixpath.normpath(posixpath.join(ATTACHMENT_DIR, folder, filename))
    if not path.startswith(ATTACHMENT_DIR + "/"):
        raise ValueError("name leaves the attachment folder")
    return path
