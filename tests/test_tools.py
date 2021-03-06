"""Tests for the `snipskit.tools` module."""

import pytest
from snipskit.tools import find_path, latest_snips_version

# Variables for some file paths we test."""
etc = '/etc/snips.toml'
usr = '/usr/local/etc/snips.toml'

# A list of the scenarios we want to test for the `find_path` function.
#
# Each item in the list is a tuple:
# (files in the file system, search path for the function, expected result)
test_data_search_path = [
    ([],         [],         None),
    ([],         [etc],      None),
    ([],         [etc, usr], None),
    ([etc],      [],         None),
    ([etc],      [etc],      etc),
    ([etc],      [etc, usr], etc),
    ([usr],      [],         None),
    ([usr],      [etc],      None),
    ([usr],      [etc, usr], usr),
    ([etc, usr], [],         None),
    ([etc, usr], [etc],      etc),
    ([etc, usr], [etc, usr], etc)
]


@pytest.mark.parametrize("file_system,files,expected", test_data_search_path)
def test_find_path(file_system, files, expected, fs):
    """Test whether the `find_path` function returns the right result
    in a couple of scenarios."""
    for filename in file_system:
        fs.create_file(filename)

    assert find_path(files) == expected

def test_latest_snips_version():
    """Test whether the `latest_snips_version` function returns the current
    latest version of Snips.

    Because a real test would just reimplement the function, we compare to a
    hardcoded string. Update this string when a new version of Snips is
    published."""

    assert latest_snips_version() == '1.1.2'
