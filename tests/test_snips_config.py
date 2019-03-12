"""Tests for the `snipskit.config.SnipsConfig` class."""

import pytest
from snipskit.config import SnipsConfig
from snipskit.exceptions import SnipsConfigNotFoundError
from toml import TomlDecodeError


def test_snips_config_default(fs):
    """Test whether a default `SnipsConfig` object is initialized correctly."""
    config_file = '/usr/local/etc/snips.toml'
    fs.create_file(config_file,
                   contents='[snips-hotword]\n'
                            'audio = ["+@mqtt"]\n')

    snips_config = SnipsConfig()
    assert snips_config.filename == config_file
    assert snips_config['snips-hotword']['audio'] == ["+@mqtt"]


def test_snips_config_with_filename(fs):
    """Test whether a `SnipsConfig` object is initialized correctly with a
    filename argument."""
    config_file = '/usr/local/etc/snips.toml'
    fs.create_file(config_file,
                   contents='[snips-hotword]\n'
                            'audio = ["+@mqtt"]\n')

    snips_config = SnipsConfig(config_file)
    assert snips_config.filename == config_file
    assert snips_config['snips-hotword']['audio'] == ["+@mqtt"]


def test_snips_config_key_not_found(fs):
    """Test whether accessing a key that doesn't exist in a `SnipsConfig`
    object raises a `KeyError`.
    """
    config_file = '/usr/local/etc/snips.toml'
    fs.create_file(config_file,
                   contents='[snips-hotword]\n'
                            'audio = ["+@mqtt"]\n')

    snips_config = SnipsConfig()
    with pytest.raises(KeyError):
        snips_config['snips-hotword']['model']


def test_snips_config_broken_toml(fs):
    """Test whether a `SnipsConfig` object raises `TomlDecodeError` when a
    broken TOML file is read.
    """
    config_file = '/etc/snips.toml'
    fs.create_file(config_file,
                   contents='[snips-hotword\n'
                            'audio = ["+@mqtt"]\n')

    with pytest.raises(TomlDecodeError):
        snips_config = SnipsConfig()


def test_snips_config_file_not_found(fs):
    """Test whether a `SnipsConfig` object raises `FileNotFoundError` when the
    specified file doesn't exist.
    """
    with pytest.raises(FileNotFoundError):
        snips_config = SnipsConfig('/etc/snips.toml')


def test_snips_config_no_config_file(fs):
    """Test whether a `SnipsConfig` object raises `SnipsConfigNotFoundError`
    when there's no snips.toml found in the search path.
    """
    with pytest.raises(SnipsConfigNotFoundError):
        snips_config = SnipsConfig()
