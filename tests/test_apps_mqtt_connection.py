"""Tests for the `snipskit.config.apps.MQTTSnipsApp` class."""

import pytest

from snipskit.apps import MQTTSnipsApp
from snipskit.app_decorators import intent, intent_not_recognized, intents, \
    session_ended, session_queued, session_started


class SimpleMQTTApp(MQTTSnipsApp):
    """A simple Snips app using MQTT directly to test."""

    def initialize(self):
        pass


def test_snips_app_mqtt_connection_default(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with the default MQTT connection
    settings connects to the MQTT broker correctly.
    """

    config_file = '/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file, contents='[snips-common]\n')
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTApp, 'initialize')

    app = SimpleMQTTApp()

    # Check configuration
    assert app.assistant['language'] == 'en'
    assert app.assistant.snips.mqtt.broker_address == 'localhost:1883'

    # Check MQTT connection
    assert app.mqtt.username_pw_set.call_count == 0
    assert app.mqtt.tls_set.call_count == 0
    assert app.mqtt.loop_forever.call_count == 1 
    app.mqtt.connect.assert_called_once_with('localhost', 1883, 60)

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1

def test_snips_app_mqtt_connection_with_authentication(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with MQTT authentication connects 
    to the MQTT broker correctly.
    """

    config_file = '/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:8883"\n'
                                         'mqtt_username = "foobar"\n'
                                         'mqtt_password = "secretpassword"\n')
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTApp, 'initialize')

    app = SimpleMQTTApp()

    # Check configuration
    assert app.assistant['language'] == 'en'
    assert app.assistant.snips.mqtt.broker_address == 'mqtt.example.com:8883'
    assert app.assistant.snips.mqtt.username == 'foobar'
    assert app.assistant.snips.mqtt.password == 'secretpassword'

    # Check MQTT connection
    app.mqtt.username_pw_set.assert_called_once_with('foobar',
                                                     'secretpassword') 
    assert app.mqtt.tls_set.call_count == 0
    assert app.mqtt.loop_forever.call_count == 1 
    app.mqtt.connect.assert_called_once_with('mqtt.example.com', 8883, 60)

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1

def test_snips_app_mqtt_connection_with_tls_and_authentication(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with TLS and MQTT authentication
    connects to the MQTT broker correctly.
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

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTApp, 'initialize')

    app = SimpleMQTTApp()

    # Check configuration
    assert app.assistant['language'] == 'en'
    assert app.assistant.snips.mqtt.broker_address == 'mqtt.example.com:4883'
    assert app.assistant.snips.mqtt.username == 'foobar'
    assert app.assistant.snips.mqtt.password == 'secretpassword'
    assert app.assistant.snips.mqtt.tls_hostname == 'mqtt.example.com'
    assert app.assistant.snips.mqtt.tls_ca_file == '/etc/ssl/certs/ca-certificates.crt'

    # Check MQTT connection
    app.mqtt.username_pw_set.assert_called_once_with('foobar',
                                                     'secretpassword') 
    app.mqtt.tls_set.assert_called_once_with(ca_certs='/etc/ssl/certs/ca-certificates.crt',
                                             certfile=None,
                                             keyfile=None)
    assert app.mqtt.loop_forever.call_count == 1 
    app.mqtt.connect.assert_called_once_with('mqtt.example.com', 4883, 60)

    # Check whether `initialize()` method is called.
    assert app.initialize.call_count == 1
