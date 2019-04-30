"""Tests for the decorators for the `snipskit.components.MQTTSnipsComponent`
class.
"""

from snipskit.mqtt.components import MQTTSnipsComponent


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
    mocker.spy(MQTTSnipsComponent, '_subscribe_topics')

    component = MQTTSnipsComponent()

    @component.topic('hermes/intent/#')
    def handle_intents(topic, payload):
        pass

    component.run()

    # Simulate the call of `_subscribe_topics` when the client connects to MQTT
    component._subscribe_topics(None, None, None, None)
    # Check whether the right callback is added.
    component.mqtt.subscribe.assert_called_once_with('hermes/intent/#')
    component.mqtt.message_callback_add.assert_called_once_with('hermes/intent/#',
                                                                handle_intents)
