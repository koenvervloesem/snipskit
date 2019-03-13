"""Tests for the `snipskit.config.apps.MQTTSnipsApp` class."""

from snipskit.apps import MQTTSnipsApp
from snipskit.app_decorators import topic


class DecoratedMQTTApp(MQTTSnipsApp):
    """A simple Snips app using MQTT directly to test."""

    def initialize(self):
        pass

    def do_something():
        pass

    @topic('hermes/intent/#')
    def handle_intents(self, client, userdata, msg):
        pass


def test_snips_app_mqtt_decorators(fs, mocker):
    """Test whether a `MQTTSnipsApp` object with callbacks using the @topic
    decorator is initialized correctly.
    """

    config_file = '/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file, contents='[snips-common]\n')
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.subscribe')
    mocker.patch('paho.mqtt.client.Client.message_callback_add')
    mocker.spy(DecoratedMQTTApp, '_subscribe_topics')

    app = DecoratedMQTTApp()

    # Check if the callback method has the attribute `topic` and other methods
    # don't.
    assert app.handle_intents.topic == 'hermes/intent/#'
    assert not hasattr(app.do_something, 'topic')

    # Simulate the call of `_subscribe_topics` when the client connects to MQTT
    app._subscribe_topics(None, None, None, None)
    # Check whether the right callback is called.
    assert app._subscribe_topics.call_count == 1 
    app.mqtt.subscribe.assert_called_once_with('hermes/intent/#') 
    app.mqtt.message_callback_add.assert_called_once_with('hermes/intent/#',
                                                          app.handle_intents) 
