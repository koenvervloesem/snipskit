"""This module contains decorators_ to apply to methods of a
:class:`.HermesSnipsComponent` object.

.. _decorators: https://docs.python.org/3/glossary.html#term-decorator

By applying one of these decorators to a method of a
:class:`.HermesSnipsComponent` object, this method is registered as a callback
to the corresponding event. When the event fires (e.g. an intent happens), the
method is called.

Example:

.. code-block:: python

    from snipskit.hermes.apps import HermesSnipsApp
    from snipskit.hermes.decorators import intent

    class SimpleSnipsApp(HermesSnipsApp):

        @intent('User:ExampleIntent')
        def example_intent(self, hermes, intent_message):
            print('I received intent "User:ExampleIntent"')
"""


def intent(intent_name):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the intent `intent_name`
    is recognized.

    Args:
        intent_name (str): The intent you want to subscribe to.

    """
    def inner(method):
        """The method to apply the decorator to."""
        method.subscribe_method = 'subscribe_intent'
        method.subscribe_parameter = intent_name
        return method
    return inner


def intent_not_recognized(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    doesn't recognize an intent.
    """
    method.subscribe_method = 'subscribe_intent_not_recognized'
    return method


def intents(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered everytime an intent is
    recognized.
    """
    method.subscribe_method = 'subscribe_intents'
    return method


def session_ended(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager ends
    a session.
    """
    method.subscribe_method = 'subscribe_session_ended'
    return method


def session_queued(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    queues the current session.
    """
    method.subscribe_method = 'subscribe_session_queued'
    return method


def session_started(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    queues starts a new session.
    """
    method.subscribe_method = 'subscribe_session_started'
    return method
