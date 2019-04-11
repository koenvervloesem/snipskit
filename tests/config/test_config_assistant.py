"""Tests for the `snipskit.config.AssistantConfig` class."""

from json import JSONDecodeError

import pytest
from snipskit.config import AssistantConfig
from snipskit.exceptions import AssistantConfigNotFoundError


def test_assistant_config_default(fs):
    """Test whether a default `AssistantConfig` object is initialized
    correctly.
    """
    assistant_file = '/usr/local/etc/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    assistant_config = AssistantConfig()
    assert assistant_config.filename == assistant_file
    assert assistant_config['language'] == 'en'


def test_assistant_config_with_filename(fs):
    """Test whether an `AssistantConfig` object is initialized correctly with a
    filename argument.
    """
    assistant_file = '/opt/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    assistant_config = AssistantConfig(assistant_file)
    assert assistant_config.filename == assistant_file
    assert assistant_config['language'] == 'en'


def test_assistant_config_key_not_found(fs):
    """Test whether accessing a key that doesn't exist in an `AssistantConfig`
    object raises a `KeyError`.
    """
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    assistant_config = AssistantConfig()
    with pytest.raises(KeyError):
        assistant_config['name']


def test_assistant_config_broken_json(fs):
    """Test whether an `AssistantConfig` object raises `JSONDecodeError` when a
    broken JSON file is read.
    """
    assistant_file = '/usr/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en", }')

    with pytest.raises(JSONDecodeError):
        assistant_config = AssistantConfig()


def test_assistant_config_file_not_found(fs):
    """Test whether an `AssistantConfig` object raises `FileNotFoundError` when
    the specified assistant configuration file doesn't exist.
    """
    with pytest.raises(FileNotFoundError):
        assistant_config = AssistantConfig('/opt/assistant/assistant.json')


def test_assistant_config_no_config_file(fs):
    """Test whether an `AssistantConfig` object raises
    `AssistantConfigNotFoundError` when there's no assistant configuration
    found in the search path.
    """
    with pytest.raises(AssistantConfigNotFoundError):
        assistant_config = AssistantConfig()
