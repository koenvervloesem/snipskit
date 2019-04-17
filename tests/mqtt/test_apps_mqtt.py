"""Tests for the `snipskit.apps.MQTTSnipsApp` class."""

from snipskit.mqtt.apps import MQTTSnipsApp
from snipskit.config import AppConfig, SnipsConfig


class SimpleMQTTApp(MQTTSnipsApp):
    """A simple Snips app using MQTT directly to test."""

    def initialize(self):
        pass


def test_snips_app_mqtt_default(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with the default parameters is set
    up correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTApp, 'initialize')

    app = SimpleMQTTApp()

    # Check Snips configuration
    assert app.snips.mqtt.broker_address == 'localhost:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check there's no app configuration
    assert app.config is None

    # Check MQTT connection
    assert app.mqtt.username_pw_set.call_count == 0
    assert app.mqtt.tls_set.call_count == 0
    assert app.mqtt.loop_forever.call_count == 1
    app.mqtt.connect.assert_called_once_with('localhost', 1883, 60, '')

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_mqtt_default_with_assistant_path(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with the default parameters and an
    assistant configuration path in snips.toml is set up correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'assistant = "/opt/assistant"\n')

    assistant_file = '/opt/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTApp, 'initialize')

    app = SimpleMQTTApp()

    # Check Snips configuration
    assert app.snips.mqtt.broker_address == 'localhost:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check there's no app configuration
    assert app.config is None

    # Check MQTT connection
    assert app.mqtt.username_pw_set.call_count == 0
    assert app.mqtt.tls_set.call_count == 0
    assert app.mqtt.loop_forever.call_count == 1
    app.mqtt.connect.assert_called_once_with('localhost', 1883, 60, '')

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_mqtt_snips_config(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with a SnipsConfig parameter is
    set up correctly.
    """

    config_file = '/opt/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:1883"\n')

    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTApp, 'initialize')

    snips_config = SnipsConfig(config_file)
    app = SimpleMQTTApp(snips=snips_config)

    # Check Snips configuration
    assert app.snips == snips_config
    assert app.snips.mqtt.broker_address == 'mqtt.example.com:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check there's no app configuration
    assert app.config is None

    # Check MQTT connection
    assert app.mqtt.username_pw_set.call_count == 0
    assert app.mqtt.tls_set.call_count == 0
    assert app.mqtt.loop_forever.call_count == 1
    app.mqtt.connect.assert_called_once_with('mqtt.example.com', 1883, 60, '')

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_mqtt_config(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with an app configuration is set
    up correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(assistant_file, contents='{"language": "en"}')

    app_config_file = 'config.ini'
    fs.create_file(app_config_file, contents='[secret]\n'
                                             'api-key=foobar\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTApp, 'initialize')

    app_config = AppConfig()
    app = SimpleMQTTApp(config=app_config)

    # Check Snips configuration
    assert app.snips.mqtt.broker_address == 'localhost:1883'

    # Check assistant configuration
    assert app.assistant['language'] == 'en'

    # Check the app configuration
    assert app.config == app_config
    assert app.config.filename == app_config_file
    assert app.config['secret']['api-key'] == 'foobar'

    # Check MQTT connection
    assert app.mqtt.username_pw_set.call_count == 0
    assert app.mqtt.tls_set.call_count == 0
    assert app.mqtt.loop_forever.call_count == 1
    app.mqtt.connect.assert_called_once_with('localhost', 1883, 60, '')

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1
