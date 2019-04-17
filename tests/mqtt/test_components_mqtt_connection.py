"""Tests for the `snipskit.components.MQTTSnipsComponent` class."""

from snipskit.mqtt.components import MQTTSnipsComponent
from snipskit.config import SnipsConfig


class SimpleMQTTComponent(MQTTSnipsComponent):
    """A simple Snips component using MQTT directly to test."""

    def initialize(self):
        pass


def test_snips_component_mqtt_connection_default(fs, mocker):
    """Test whether a `MQTTSnipsComponent` object with the default MQTT
    connection settings connects to the MQTT broker correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTComponent, 'initialize')

    component = SimpleMQTTComponent()

    # Check configuration
    assert component.snips.mqtt.broker_address == 'localhost:1883'

    # Check MQTT connection
    assert component.mqtt.username_pw_set.call_count == 0
    assert component.mqtt.tls_set.call_count == 0
    assert component.mqtt.loop_forever.call_count == 1
    component.mqtt.connect.assert_called_once_with('localhost', 1883, 60, '')

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1


def test_snips_component_mqtt_with_snips_config(fs, mocker):
    """Test whether a `MQTTSnipsComponent` object with a `SnipsConfig` object
    passed to `__init__` uses the connection settings from the specified file.
    """

    config_file = 'snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:1883"\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTComponent, 'initialize')

    snips_config = SnipsConfig(config_file)
    component = SimpleMQTTComponent(snips_config)

    # Check configuration
    assert component.snips == snips_config
    assert component.snips.mqtt.broker_address == 'mqtt.example.com:1883'

    # Check MQTT connection
    assert component.mqtt.username_pw_set.call_count == 0
    assert component.mqtt.tls_set.call_count == 0
    assert component.mqtt.loop_forever.call_count == 1
    component.mqtt.connect.assert_called_once_with('mqtt.example.com', 1883,
                                                   60, '')

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1


def test_snips_component_mqtt_connection_with_authentication(fs, mocker):
    """Test whether a `MQTTSnipsComponent` object with MQTT authentication
    connects to the MQTT broker correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:8883"\n'
                                         'mqtt_username = "foobar"\n'
                                         'mqtt_password = "secretpassword"\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTComponent, 'initialize')

    component = SimpleMQTTComponent()

    # Check configuration
    assert component.snips.mqtt.broker_address == 'mqtt.example.com:8883'
    assert component.snips.mqtt.username == 'foobar'
    assert component.snips.mqtt.password == 'secretpassword'

    # Check MQTT connection
    component.mqtt.username_pw_set.assert_called_once_with('foobar',
                                                           'secretpassword')
    assert component.mqtt.tls_set.call_count == 0
    assert component.mqtt.loop_forever.call_count == 1
    component.mqtt.connect.assert_called_once_with('mqtt.example.com', 8883,
                                                   60, '')

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1


def test_snips_component_mqtt_connection_with_tls_and_authentication(fs, mocker):
    """Test whether a `MQTTSnipsComponent` object with TLS and MQTT
    authentication connects to the MQTT broker correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file,
                   contents='[snips-common]\n'
                            'mqtt = "mqtt.example.com:4883"\n'
                            'mqtt_username = "foobar"\n'
                            'mqtt_password = "secretpassword"\n'
                            'mqtt_tls_hostname="mqtt.example.com"\n'
                            'mqtt_tls_cafile="/etc/ssl/certs/ca-certificates.crt"\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.tls_set')
    mocker.patch('paho.mqtt.client.Client.username_pw_set')
    mocker.patch.object(SimpleMQTTComponent, 'initialize')

    component = SimpleMQTTComponent()

    # Check configuration
    assert component.snips.mqtt.broker_address == 'mqtt.example.com:4883'
    assert component.snips.mqtt.username == 'foobar'
    assert component.snips.mqtt.password == 'secretpassword'
    assert component.snips.mqtt.tls_hostname == 'mqtt.example.com'
    assert component.snips.mqtt.tls_ca_file == '/etc/ssl/certs/ca-certificates.crt'

    # Check MQTT connection
    component.mqtt.username_pw_set.assert_called_once_with('foobar',
                                                           'secretpassword')
    component.mqtt.tls_set.assert_called_once_with(ca_certs='/etc/ssl/certs/ca-certificates.crt',
                                                   certfile=None,
                                                   keyfile=None)
    assert component.mqtt.loop_forever.call_count == 1
    component.mqtt.connect.assert_called_once_with('mqtt.example.com', 4883,
                                                   60, '')

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1
