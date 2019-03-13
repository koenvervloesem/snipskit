"""Tests for the `snipskit.config.apps.HermesSnipsApp` class."""

from snipskit.apps import HermesSnipsApp
from snipskit.app_decorators import intent, intent_not_recognized, intents, \
    session_ended, session_queued, session_started


class DecoratedHermesApp(HermesSnipsApp):

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


def test_snips_app_hermes_decorators(fs, mocker):
    """Test whether a `HermesSnipsApp` object with callbacks using decorators
    is initialized correctly.
    """

    config_file = '/etc/snips.toml'
    assistant_file = '/usr/local/share/snips/assistant/assistant.json'
    fs.create_file(config_file, contents='[snips-common]\n')
    fs.create_file(assistant_file, contents='{"language": "en"}')

    mocker.patch('hermes_python.hermes.Hermes.connect')
    mocker.patch('hermes_python.hermes.Hermes.loop_forever')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_intent')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_intent_not_recognized')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_intents')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_session_ended')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_session_queued')
    mocker.patch('hermes_python.hermes.Hermes.subscribe_session_started')

    app = DecoratedHermesApp()

    assert app.callback_intent1.intent == 'koan:Intent1'
    app.hermes.subscribe_intent.assert_called_once_with('koan:Intent1', app.callback_intent1)

    assert app.callback_intent_not_recognized.intent_not_recognized is True
    app.hermes.subscribe_intent_not_recognized.assert_called_once_with(app.callback_intent_not_recognized)

    assert app.callback_intents.intents is True
    app.hermes.subscribe_intents.assert_called_once_with(app.callback_intents)

    assert app.callback_session_ended.session_ended is True
    app.hermes.subscribe_session_ended.assert_called_once_with(app.callback_session_ended)

    assert app.callback_session_queued.session_queued is True
    app.hermes.subscribe_session_queued.assert_called_once_with(app.callback_session_queued)

    assert app.callback_session_started.session_started is True
    app.hermes.subscribe_session_started.assert_called_once_with(app.callback_session_started)

