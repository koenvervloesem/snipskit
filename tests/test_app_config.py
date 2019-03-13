"""Tests for the `snipskit.config.AppConfig` class."""

from snipskit.config import AppConfig


def test_app_config_default(fs):
    """Test whether a default `AppConfig` object is initialized
    correctly.
    """
    config_file = 'config.ini'
    fs.create_file(config_file, contents='[secret]\n'
                                         'api-key=foobar\n')

    app_config = AppConfig()
    assert app_config.filename == config_file
    assert app_config['secret']['api-key'] == 'foobar'


def test_app_config_path(fs):
    """Test whether an `AppConfig` object is initialized with the correct
    filename.
    """
    config_file = 'foobar.ini'
    fs.create_file(config_file, contents='[secret]\n'
                                         'api-key=foobar\n')

    app_config = AppConfig(config_file)
    assert app_config.filename == config_file
    assert app_config['secret']['api-key'] == 'foobar'


def test_app_config_write(fs):
    """Test whether we can write an `AppConfig` object.
    """
    config_file = 'config.ini'
    fs.create_file(config_file, contents='[secret]\n'
                                         'api-key=foobar\n')

    app_config = AppConfig()
    app_config['secret']['api-key'] = 'barfoo'

    assert app_config['secret']['api-key'] == 'barfoo'

    app_config.write()

    app_config2 = AppConfig()
    assert app_config2['secret']['api-key'] == 'barfoo'


def test_app_config_write_with_filename(fs):
    """Test whether we can write an `AppConfig` object with a filename
    argument.
    """
    config_file = 'config.ini'
    fs.create_file(config_file, contents='[secret]\n'
                                         'api-key=foobar\n')

    app_config = AppConfig()
    app_config['secret']['api-key'] = 'barfoo'

    with open('config.ini', 'wt') as config:
        app_config.write(config)

    app_config2 = AppConfig()
    assert app_config2['secret']['api-key'] == 'barfoo'
