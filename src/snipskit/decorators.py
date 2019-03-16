"""This module contains decorators to add to methods of a Snips component.

By applying one of these decorators to a method of a :obj:`SnipsComponent`
object, this method is registered as a callback to the corresponding event.
When the event fires (e.g. an intent happens), the method is called.

Example:

.. code-block:: python

    from snipskit.apps import HermesSnipsApp
    from snipskit.decorators import intent

    class SimpleSnipsApp(HermesSnipsApp):

        @intent('User:ExampleIntent')
        def example_intent(self, hermes, intent_message):
            print('I received intent "User:ExampleIntent"')
"""


# Decorators for MQTTSnipsComponent
def topic(topic_name):
    """Apply this decorator to a method of class :obj:`MQTTSnipsComponent`
    to register it as a callback to be triggered when the MQTT topic
    `topic_name` is published.

    Attributes:
        topic_name (str): The MQTT topic you want to subscribe to.
    """
    def inner(function):
        function.topic = topic_name
        return function
    return inner


# Decorators for HermesSnipsComponent
def intent(intent_name):
    """Apply this decorator to a method of class :obj:`HermesSnipsComponent`
    to register it as a callback to be triggered when the intent `intent_name`
    is recognized.

    Attributes:
        intent_name (str): The intent you want to subscribe to.

    """
    def inner(function):
        function.intent = intent_name
        return function
    return inner


def intent_not_recognized(function):
    """Apply this decorator to a method of class :obj:`HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    doesn't recognize an intent.
    """
    function.intent_not_recognized = True
    return function


def intents(function):
    """Apply this decorator to a method of class :obj:`HermesSnipsComponent`
    to register it as a callback to be triggered everytime an intent is
    recognized.
    """
    function.intents = True
    return function


def session_ended(function):
    """Apply this decorator to a method of class :obj:`HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager ends
    a session.
    """
    function.session_ended = True
    return function


def session_queued(function):
    """Apply this decorator to a method of class :obj:`HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    queues the current session.
    """
    function.session_queued = True
    return function


def session_started(function):
    """Apply this decorator to a method of class :obj:`HermesSnipsComponent`
    to register it as a callback to be triggered when the dialogue manager
    queues starts a new session.
    """
    function.session_started = True
    return function
