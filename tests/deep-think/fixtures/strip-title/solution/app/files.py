def base_name(filename):
    """Remove the .txt extension from a file name."""
    if filename.endswith(".txt"):
        return filename[:-len(".txt")]
    return filename
