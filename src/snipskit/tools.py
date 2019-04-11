"""This module contains some useful tools for the snipskit library."""

from pathlib import Path
import re
from urllib.request import urlopen

# Workaround for occasional errors when downloading the release notes.
import http.client
http.client._MAXHEADERS = 1000

_RELEASE_NOTES_URL = 'https://docs.snips.ai/additional-resources/release-notes'
_LATEST_VERSION_REGEX = r'<span data-offset-key="\S*">Platform Update (\d*\.\d*\.\d*)\s'


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

def latest_snips_version():
    """Return the latest version of Snips, as published in the release notes.

    Returns:
        str: The latest version of Snips.

    Raises:
        URLError: When the function runs into a problem downloading the release
        notes.
    """
    url = urlopen(_RELEASE_NOTES_URL)
    release_notes = url.read().decode('utf-8')
    versions = re.findall(_LATEST_VERSION_REGEX, release_notes)
    return max(versions)
