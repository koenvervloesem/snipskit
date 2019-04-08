"""Tests for the decorators for the `snipskit.components.MQTTSnipsComponent`
class.
"""

from snipskit.mqtt.components import MQTTSnipsComponent
from snipskit.mqtt.decorators import topic


class DecoratedMQTTComponent(MQTTSnipsComponent):
    """A simple Snips component using MQTT directly to test."""

    def initialize(self):
        pass

    def do_something(self):
        pass

    @topic('hermes/intent/#')
    def handle_intents(self, topic, payload):
        pass


def test_snips_component_mqtt_decorators(fs, mocker):
    """Test whether a `MQTTSnipsComponent` object with callbacks using the
    @topic decorator is initialized correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.subscribe')
    mocker.patch('paho.mqtt.client.Client.message_callback_add')
    mocker.spy(DecoratedMQTTComponent, '_subscribe_topics')

    component = DecoratedMQTTComponent()

    # Check if the callback method has the attribute `topic` and other methods
    # don't.
    assert component.handle_intents.topic == 'hermes/intent/#'
    assert not hasattr(component.do_something, 'topic')

    # Simulate the call of `_subscribe_topics` when the client connects to MQTT
    component._subscribe_topics(None, None, None, None)
    # Check whether the right callback is called.
    assert component._subscribe_topics.call_count == 1
    component.mqtt.subscribe.assert_called_once_with('hermes/intent/#')
    component.mqtt.message_callback_add.assert_called_once_with('hermes/intent/#',
                                                                component.handle_intents)
