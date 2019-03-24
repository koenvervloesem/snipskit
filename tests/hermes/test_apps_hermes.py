"""Tests for the `snipskit.apps.hermes.HermesSnipsApp` class."""

from snipskit.hermes.apps import HermesSnipsApp
from snipskit.config import AppConfig, SnipsConfig


class SimpleHermesApp(HermesSnipsApp):
    """A simple Snips app using Hermes to test."""

    def initialize(self):
        pass


def test_snips_app_hermes_default(fs, mocker):
    """Test whether a `HermesSnipsApp` object with the default parameters is
    set up correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesApp, 'initialize')

    app = SimpleHermesApp()

    # Check Snips configuration
    assert app.snips.mqtt.broker_address == 'localhost:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check there's no app configuration
    assert app.config is None

    # Check MQTT connection
    assert app.hermes.mqtt_options.broker_address == app.snips.mqtt.broker_address
    assert app.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_hermes_default_with_assistant_path(fs, mocker):
    """Test whether a `HermesSnipsApp` object with the default parameters and
    an assistant configuration path in snips.toml is set up correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'assistant = "/opt/assistant"\n')

    assistant_file = '/opt/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesApp, 'initialize')

    app = SimpleHermesApp()

    # Check Snips configuration
    assert app.snips.mqtt.broker_address == 'localhost:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check there's no app configuration
    assert app.config is None

    # Check MQTT connection
    assert app.hermes.mqtt_options.broker_address == app.snips.mqtt.broker_address
    assert app.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_hermes_snips_config(fs, mocker):
    """Test whether a `HermesSnipsapp` object with a SnipsConfig parameter is
    set up correctly.
    """

    config_file = '/opt/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:1883"\n')

    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesApp, 'initialize')

    snips_config = SnipsConfig(config_file)
    app = SimpleHermesApp(snips=snips_config)

    # Check Snips configuration
    assert app.snips == snips_config
    assert app.snips.mqtt.broker_address == 'mqtt.example.com:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check there's no app configuration
    assert app.config is None

    # Check MQTT connection
    assert app.hermes.mqtt_options.broker_address == app.snips.mqtt.broker_address
    assert app.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_hermes_config(fs, mocker):
    """Test whether a `HermesSnipsApp` object with an app configuration is set
    up correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    app_config_file = 'config.ini'
    fs.create_file(app_config_file, contents='[secret]\n'
                                             'api-key=foobar\n')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesApp, 'initialize')

    app_config = AppConfig()
    app = SimpleHermesApp(config=app_config)

    # Check Snips configuration
    assert app.snips.mqtt.broker_address == 'localhost:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check the app configuration
    assert app.config == app_config
    assert app.config.filename == app_config_file
    assert app.config['secret']['api-key'] == 'foobar'

    # Check MQTT connection
    assert app.hermes.mqtt_options.broker_address == app.snips.mqtt.broker_address
    assert app.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1
