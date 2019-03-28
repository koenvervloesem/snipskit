"""Tests for the decorators for the `snipskit.components.HermesSnipsComponent`
class.
"""

from snipskit.hermes.components import HermesSnipsComponent
from snipskit.hermes.decorators import intent, intent_not_recognized, \
    intents, session_ended, session_queued, session_started


class DecoratedHermesComponent(HermesSnipsComponent):

    @intent('koan:Intent1')
    def callback_intent1(self, hermes, intent_message):
        pass

    @intent_not_recognized
    def callback_intent_not_recognized(self, hermes, intent_message):
        pass

    @intents
    def callback_intents(self, hermes, intent_message):
        pass

    @session_ended
    def callback_session_ended(self, hermes, session_ended_message):
        pass

    @session_queued
    def callback_session_queued(self, hermes, session_queued_message):
        pass

    @session_started
    def callback_session_started(self, hermes, session_started_message):
        pass


def test_snips_component_hermes_decorators(fs, mocker):
    """Test whether a `HermesSnipsComponent` object with callbacks using
    decorators is initialized correctly.
    """

    config_file = '/etc/snips.toml'
    fs.create_file(config_file, contents='[snips-common]\n')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_intent')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_intent_not_recognized')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_intents')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_session_ended')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_session_queued')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_session_started')

    component = DecoratedHermesComponent()

    assert component.callback_intent1.subscribe_method == 'subscribe_intent'
    assert component.callback_intent1.subscribe_parameter == 'koan:Intent1'
    component.hermes.subscribe_intent.assert_called_once_with('koan:Intent1',
                                                              component.callback_intent1)

    assert component.callback_intent_not_recognized.subscribe_method == 'subscribe_intent_not_recognized'
    component.hermes.subscribe_intent_not_recognized.assert_called_once_with(component.callback_intent_not_recognized)

    assert component.callback_intents.subscribe_method == 'subscribe_intents'
    component.hermes.subscribe_intents.assert_called_once_with(component.callback_intents)

    assert component.callback_session_ended.subscribe_method == 'subscribe_session_ended'
    component.hermes.subscribe_session_ended.assert_called_once_with(component.callback_session_ended)

    assert component.callback_session_queued.subscribe_method == 'subscribe_session_queued'
    component.hermes.subscribe_session_queued.assert_called_once_with(component.callback_session_queued)

    assert component.callback_session_started.subscribe_method == 'subscribe_session_started'
    component.hermes.subscribe_session_started.assert_called_once_with(component.callback_session_started)
