"""This module contains some useful tools for the snipskit library."""

from pathlib import Path


def find_path(paths):
    """Given a search path of files or directories with absolute paths, find
    the first existing path.

    Args:
        paths (list): A list of strings with absolute paths.

    Returns:
        string: The first path in the list `paths` that exists, or `None` if
        none of the paths exist.

    Example:
        The following example works if the file system has a file
        /usr/local/etc/snips.toml (e.g. on macOS with Snips installed):

        >>> find_path(['/etc/snips.toml', '/usr/local/etc/snips.toml'])
        '/usr/local/etc/snips.toml'
    """
    for name in paths:
        path = Path(name)
        if path.exists():
            return str(path.resolve())

    # If none of the paths in the search path are found in the file system,
    # return None.
    return None
