"""Tests for the `snipskit.components.HermesSnipsComponent` class."""

from snipskit.components import HermesSnipsComponent
from snipskit.config import SnipsConfig


class SimpleHermesComponent(HermesSnipsComponent):
    """A simple Snips component using Hermes to test."""

    def initialize(self):
        pass


def test_snips_component_hermes_connection_default(fs, mocker):
    """Test whether a `HermesSnipsComponent` object with the default MQTT
    connection settings sets up its `Hermes` object correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesComponent, 'initialize')

    component = SimpleHermesComponent()

    # Check configuration
    assert component.snips.mqtt.broker_address == 'localhost:1883'

    # Check MQTT connection
    assert component.hermes.mqtt_options == component.snips.mqtt
    assert component.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1


def test_snips_component_hermes_with_snips_config(fs, mocker):
    """Test whether a `HermesSnipsComponent` object with a `SnipsConfig` object
    passed to `__init__` uses the connection settings from the specified file.
    """

    config_file = 'snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:1883"\n')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesComponent, 'initialize')

    snips_config = SnipsConfig(config_file)
    component = SimpleHermesComponent(snips_config)

    # Check configuration
    assert component.snips == snips_config
    assert component.snips.mqtt.broker_address == 'mqtt.example.com:1883'

    # Check MQTT connection
    assert component.hermes.mqtt_options == component.snips.mqtt
    assert component.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1


def test_snips_component_hermes_connection_with_authentication(fs, mocker):
    """Test whether a `HermesSnipsComponent` object with MQTT authentication
    settings sets up its `Hermes` object correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n'
                                         'mqtt = "mqtt.example.com:8883"\n'
                                         'mqtt_username = "foobar"\n'
                                         'mqtt_password = "secretpassword"\n')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesComponent, 'initialize')

    component = SimpleHermesComponent()

    # Check configuration
    assert component.snips.mqtt.broker_address == 'mqtt.example.com:8883'
    assert component.snips.mqtt.username == 'foobar'
    assert component.snips.mqtt.password == 'secretpassword'

    # Check MQTT connection
    assert component.hermes.mqtt_options == component.snips.mqtt
    assert component.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1


def test_snips_component_hermes_connection_with_tls_and_authentication(fs, mocker):
    """Test whether a `HermesSnipsComponent` object with TLS and MQTT
    authentication settings sets up its `Hermes` object correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file,
                   contents='[snips-common]\n'
                            'mqtt = "mqtt.example.com:4883"\n'
                            'mqtt_username = "foobar"\n'
                            'mqtt_password = "secretpassword"\n'
                            'mqtt_tls_hostname="mqtt.example.com"\n'
                            'mqtt_tls_cafile="/etc/ssl/certs/ca-certificates.crt"\n')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.spy(SimpleHermesComponent, 'initialize')

    component = SimpleHermesComponent()

    # Check configuration
    assert component.snips.mqtt.broker_address == 'mqtt.example.com:4883'
    assert component.snips.mqtt.username == 'foobar'
    assert component.snips.mqtt.password == 'secretpassword'
    assert component.snips.mqtt.tls_hostname == 'mqtt.example.com'
    assert component.snips.mqtt.tls_ca_file == '/etc/ssl/certs/ca-certificates.crt'

    # Check MQTT connection
    assert component.hermes.mqtt_options == component.snips.mqtt
    assert component.hermes.loop_forever.call_count == 1

    # Check whether `initialize()` method is called.
    assert component.initialize.call_count == 1
