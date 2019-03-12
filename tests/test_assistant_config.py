"""Tests for the `snipskit.config.AssistantConfig` class."""

from json import JSONDecodeError

import pytest
from snipskit.config import AssistantConfig, SnipsConfig
from snipskit.exceptions import AssistantConfigNotFoundError


def test_assistant_config_default(fs):
    """Test whether a default `AssistantConfig` object is initialized
    correctly.
    """
    config_file = '/usr/local/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file)
    fs.create_file(assistant_file, contents='{"language": "en"}')

    assistant_config = AssistantConfig()
    assert assistant_config.filename == assistant_file
    assert assistant_config.snips.filename == config_file
    assert assistant_config['language'] == 'en'


def test_assistant_config_with_snips_config(fs):
    """Test whether an `AssistantConfig` object is initialized correctly with a
    `SnipsConfig` argument.
    """
    config_file = '/usr/local/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file)
    fs.create_file(assistant_file, contents='{"language": "en"}')

    snips_config = SnipsConfig()
    assistant_config = AssistantConfig(snips_config)
    assert assistant_config.filename == assistant_file
    assert assistant_config.snips == snips_config
    assert assistant_config['language'] == 'en'


def test_assistant_config_key_not_found(fs):
    """Test whether accessing a key that doesn't exist in an `AssistantConfig`
    object raises a `KeyError`.
    """
    config_file = '/usr/local/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file)
    fs.create_file(assistant_file, contents='{"language": "en"}')

    assistant_config = AssistantConfig()
    with pytest.raises(KeyError):
        assistant_config['name']


def test_assistant_config_broken_json(fs):
    """Test whether an `AssistantConfig` object raises `JSONDecodeError` when a
    broken JSON file is read.
    """
    config_file = '/etc/snips.toml'
    assistant_file = '/usr/share/snips/assistant/assistant.json'
    fs.create_file(config_file)
    fs.create_file(assistant_file, contents='{"language": "en", }')

    with pytest.raises(JSONDecodeError):
        assistant_config = AssistantConfig()


def test_assistant_config_file_not_found(fs):
    """Test whether an `AssistantConfig` object raises `FileNotFoundError` when
    the assistant directory specified in the Snips configuration doesn't exist.
    """
    config_file = '/etc/snips.toml'
    toml_content = '[snips-common]\n' \
                   'assistant = "/usr/share/snips/assistant"\n'
    fs.create_file(config_file,
                   contents=toml_content)

    with pytest.raises(FileNotFoundError):
        assistant_config = AssistantConfig()


def test_assistant_config_no_config_file(fs):
    """Test whether an `AssistantConfig` object raises
    `AssistantConfigNotFoundError` when there's no assistant configuration
    found in the search path.
    """
    config_file = '/etc/snips.toml'
    fs.create_file(config_file)

    with pytest.raises(AssistantConfigNotFoundError):
        assistant_config = AssistantConfig()
