"""Tests for the `snipskit.config.apps.HermesSnipsApp` class."""

import pytest

from hermes_python.hermes import Hermes
from snipskit.apps import HermesSnipsApp
from snipskit.app_decorators import intent, intent_not_recognized, intents, \
    session_ended, session_queued, session_started


class SimpleHermesApp(HermesSnipsApp):
    """A simple Snips app using Hermes to test."""

    def initialize(self):
        pass

def test_snips_app_hermes_connection_default(fs, mocker):
    """Test whether a `HermesSnipsApp` object with the default MQTT connection
    settings sets up its `Hermes` object correctly. 
    """

    config_file = '/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file, contents='[snips-common]\n')
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesApp, 'initialize')

    app = SimpleHermesApp()

    # Check configuration
    assert app.assistant['language'] == 'en'
    assert app.assistant.snips.mqtt.broker_address == 'localhost:1883'

    # Check MQTT connection 
    assert app.hermes.mqtt_options == app.assistant.snips.mqtt
    assert app.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_hermes_connection_with_authentication(fs, mocker):
    """Test whether a `HermesSnipsApp` object with MQTT authentication settings
    sets up its `Hermes` object correctly.
    """

    config_file = '/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:8883"\n'
                                         'mqtt_username = "foobar"\n'
                                         'mqtt_password = "secretpassword"\n')
    fs.create_file(assistant_file, contents='{"language": "en"}')


    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesApp, 'initialize')

    app = SimpleHermesApp()

    # Check configuration
    assert app.assistant['language'] == 'en'
    assert app.assistant.snips.mqtt.broker_address == 'mqtt.example.com:8883'
    assert app.assistant.snips.mqtt.username == 'foobar'
    assert app.assistant.snips.mqtt.password == 'secretpassword'

    # Check MQTT connection 
    assert app.hermes.mqtt_options == app.assistant.snips.mqtt
    assert app.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1


def test_snips_app_hermes_connection_with_tls_and_authentication(fs, mocker):
    """Test whether a `HermesSnipsApp` object with TLS and MQTT authentication
    settings sets up its `Hermes` object correctly.
    """

    config_file = '/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file,
                   contents='[snips-common]\n'
                            'mqtt = "mqtt.example.com:4883"\n'
                            'mqtt_username = "foobar"\n'
                            'mqtt_password = "secretpassword"\n'
                            'mqtt_tls_hostname="mqtt.example.com"\n'
                            'mqtt_tls_cafile="/etc/ssl/certs/ca-certificates.crt"\n')

    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesApp, 'initialize')

    app = SimpleHermesApp()

    # Check configuration
    assert app.assistant['language'] == 'en'
    assert app.assistant.snips.mqtt.broker_address == 'mqtt.example.com:4883'
    assert app.assistant.snips.mqtt.username == 'foobar'
    assert app.assistant.snips.mqtt.password == 'secretpassword'
    assert app.assistant.snips.mqtt.tls_hostname == 'mqtt.example.com'
    assert app.assistant.snips.mqtt.tls_ca_file == '/etc/ssl/certs/ca-certificates.crt'

    # Check MQTT connection 
    assert app.hermes.mqtt_options == app.assistant.snips.mqtt
    assert app.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1
