import posixpath

ATTACHMENT_DIR = "/srv/attachments"


def attachment_path(folder, filename):
    """Where an attachment is stored: ATTACHMENT_DIR/folder/filename."""
    return posixpath.join(ATTACHMENT_DIR, folder, filename)
