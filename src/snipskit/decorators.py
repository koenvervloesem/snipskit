"""This module contains decorators to add to methods of a Snips component.
"""


# TODO: Better explain all these decorators: "Apply this decorator to a method
# of class X to register it as... to be triggered when ..." or something like
# that.
def topic(topic_name):
    """A decorator that adds an attribute `topic` with the MQTT topic to a
    function. This is used by the `MQTTSnipsComponent` class to register a
    method as a callback to be triggered when the MQTT topic `topic_name` is
    published.
    """
    def inner(function):
        function.topic = topic_name
        return function
    return inner


def intent(intent_name):
    """A decorator that adds an attribute `intent` with the intent name to a
    function. This is used by the `HermesSnipsComponent` class to register a
    method as a callback to be triggered when the intent `intent_name`
    is recognized.
    """
    def inner(function):
        function.intent = intent_name
        return function
    return inner


def intent_not_recognized(function):
    """A decorator that adds an attribute `intent_not_recognized` to a
    function. This is used by the `HermesSnipsComponent` class to register a
    method as a callback when the dialogue manager doesn't recognize an intent.
    """
    function.intent_not_recognized = True
    return function


def intents(function):
    """A decorator that adds an attribute `intents` to a function. This is used
    by the `HermesSnipsComponent` class to register a method as a callback to
    be triggered everytime an intent is recognized.
    """
    function.intents = True
    return function


def session_ended(function):
    """A decorator that adds an attribute `session_ended` to a function. This
    is used by the `HermesSnipsComponent` class to register a method as a
    callback when the dialogue manager ends a session.
    """
    function.session_ended = True
    return function


def session_queued(function):
    """A decorator that adds an attribute `session_queued` to a function. This
    is used by the `HermesSnipsComponent` class to register a method as a
    callback when the dialogue manager queues the current session.
    """
    function.session_queued = True
    return function


def session_started(function):
    """A decorator that adds an attribute `session_started` to a function. This
    is used by the `HermesSnipsComponent` class to register a method as a
    callback when the dialogue manager starts a new session.
    """
    function.session_started = True
    return function
