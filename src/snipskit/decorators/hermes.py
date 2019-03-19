"""This module contains decorators_ to apply to methods of a
:class:`.HermesSnipsComponent` object.

.. _decorators: https://docs.python.org/3/glossary.html#term-decorator

By applying one of these decorators to a method of a
:class:`.HermesSnipsComponent` object, this method is registered as a callback
to the corresponding event. When the event fires (e.g. an intent happens), the
method is called.

Example:

.. code-block:: python

    from snipskit.apps import HermesSnipsApp
    from snipskit.decorators.hermes import intent

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
        method.intent = intent_name
        return method
    return inner


def intent_not_recognized(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    doesn't recognize an intent.
    """
    method.intent_not_recognized = True
    return method


def intents(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered everytime an intent is
    recognized.
    """
    method.intents = True
    return method


def session_ended(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager ends
    a session.
    """
    method.session_ended = True
    return method


def session_queued(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    queues the current session.
    """
    method.session_queued = True
    return method


def session_started(method):
    """Apply this decorator to a method of class :class:`.HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    queues starts a new session.
    """
    method.session_started = True
    return method
