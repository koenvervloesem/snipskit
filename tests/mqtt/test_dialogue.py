"""Tests for the dialogue helper functions of :mod:`snipskit.mqtt.dialogue`.
"""

from snipskit.mqtt.components import MQTTSnipsComponent
from snipskit.mqtt.dialogue import DM_CONTINUE_SESSION, DM_END_SESSION,\
    continue_session, end_session


class DialogueMQTTComponent(MQTTSnipsComponent):
    """A simple Snips component using MQTT directly to test."""

    def initialize(self):
        pass


def test_dialogue_continue_session(fs, mocker):
    """Test whether the :func:`snipskit.mqtt.dialogue.continue_session`
    function works correctly with :meth:`.MQTTSnipsComponent.publish`.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.subscribe')
    mocker.patch('paho.mqtt.client.Client.message_callback_add')
    mocker.spy(DialogueMQTTComponent, 'publish')

    component = DialogueMQTTComponent()

    component.publish(*continue_session('testSessionId', 'testText'))

    component.publish.assert_called_once_with(component,
                                              DM_CONTINUE_SESSION,
                                              {'sessionId': 'testSessionId',
                                               'text': 'testText'})

def test_dialogue_end_session(fs, mocker):
    """Test whether the :func:`snipskit.mqtt.dialogue.end_session` function
    works correctly with :meth:`.MQTTSnipsComponent.publish`.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.subscribe')
    mocker.patch('paho.mqtt.client.Client.message_callback_add')
    mocker.spy(DialogueMQTTComponent, 'publish')

    component = DialogueMQTTComponent()

    component.publish(*end_session('testSessionId', 'testText'))

    component.publish.assert_called_once_with(component,
                                              DM_END_SESSION,
                                              {'sessionId': 'testSessionId',
                                               'text': 'testText'})

def test_dialogue_end_session_with_empty_text(fs, mocker):
    """Test whether the :func:`snipskit.mqtt.dialogue.end_session` function
    works correctly with :meth:`.MQTTSnipsComponent.publish` when the text is
    empty.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    mocker.patch('paho.mqtt.client.Client.connect')
    mocker.patch('paho.mqtt.client.Client.loop_forever')
    mocker.patch('paho.mqtt.client.Client.subscribe')
    mocker.patch('paho.mqtt.client.Client.message_callback_add')
    mocker.spy(DialogueMQTTComponent, 'publish')

    component = DialogueMQTTComponent()

    component.publish(*end_session('testSessionId'))

    component.publish.assert_called_once_with(component,
                                              DM_END_SESSION,
                                              {'sessionId': 'testSessionId'})
