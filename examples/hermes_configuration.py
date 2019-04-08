#!/usr/bin/env python3
"""This is an example of a Snips app using the Hermes protocol with the
SnipsKit library.

This app shows how to read the app's configuration, the assistant's
configuration and the configuration of Snips. This requires a configuration.ini
file in the same directory as the app, with a section `secret` and an option
`switch`.

You can find the documentation of this library in:

https://snipskit.readthedocs.io/
"""
from snipskit.hermes.apps import HermesSnipsApp
from snipskit.config import AppConfig
from snipskit.hermes.decorators import intent


class SimpleSnipsApp(HermesSnipsApp):

    @intent('User:TurnOn')
    def example_turn_on(self, hermes, intent_message):
        switch = self.config['secret']['switch']
        hermes.publish_end_session(intent_message.session_id,
                                   'You want me to turn on {}'.format(switch))

    @intent('User:Name')
    def example_name(self, hermes, intent_message):
        name = self.assistant['name']
        hermes.publish_end_session(intent_message.session_id,
                                   'My name is {}'.format(name))

    @intent('User:Master')
    def example_master(self, hermes, intent_message):
        try:
            master = self.snips['snips-audio-server']['bind'].split('@')[0]
        except KeyError:
            master = 'default'
        hermes.publish_end_session(intent_message.session_id,
                                   'My master site is {}'.format(master))


if __name__ == "__main__":
    SimpleSnipsApp(config=AppConfig())
