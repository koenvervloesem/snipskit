#!/usr/bin/env python3
"""This is an example of a Snips app using the Hermes protocol with the
SnipsKit library.

This app listens for an intent and answers the user.

You can find the documentation of this library in:

https://snipskit.readthedocs.io/
"""
from snipskit.apps import HermesSnipsApp
from snipskit.decorators.hermes import intent


class SimpleSnipsApp(HermesSnipsApp):

    @intent('User:ExampleIntent')
    def example_intent(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id,
                                   'I received ExampleIntent')


if __name__ == "__main__":
    SimpleSnipsApp()
