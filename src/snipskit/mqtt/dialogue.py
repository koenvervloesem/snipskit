"""This module contains some helper functions to work with MQTT messages using
the `Snips dialogue API`_.

.. _`Snips dialogue API`: https://docs.snips.ai/reference/dialogue
"""

DM_CONTINUE_SESSION = 'hermes/dialogueManager/continueSession'
DM_END_SESSION = 'hermes/dialogueManager/endSession'

def continue_session(session_id, text):
    """Return a tuple with a topic and payload for a `continueSession`_ message
    for the specified session ID and text.

    .. _`continueSession`: https://docs.snips.ai/reference/dialogue#continue-session

    Args:
        session_id (str): The session Id of the message.
        text (str): The text to say before continuing the session.

    Returns:
        (str, dict): A tuple of the topic and the payload to call
        :meth:`.MQTTSnipsComponent.publish` with.

    .. note:: The payload of a continueSession message can be much more
       complex. Other keys than sessionId and text are not supported by this
       helper function: it's aimed at just the simplest use cases.

    Example:
        You would use this function like this in a callback method of an
        :class:`.MQTTSnipsApp` object:

        >>> self.publish(*continue_session('mySessionId', 'myText'))

        This is equivalent to the much more wordy:

        >>> self.publish('hermes/dialogueManager/continueSession',
                         {'sessionId': 'mySessionId',
                          'text': 'myText'})

        .. versionadded:: 0.5.2
    """
    return (DM_CONTINUE_SESSION, {'sessionId': session_id, 'text': text})

def end_session(session_id, text=None):
    """Return a tuple with a topic and payload for an `endSession`_ message for
    the specified session ID and text.

    .. _`endSession`: https://docs.snips.ai/reference/dialogue#end-session

    Args:
        session_id (str): The session Id of the message.
        text (str, optional): The text to say before ending the session. If
            this is None, the session is ended immediately after publishing
            this message.

    Returns:
        (str, dict): A tuple of the topic and the payload to call
        :meth:`.MQTTSnipsComponent.publish` with.

    Example:
        You would use this function like this in a callback method of an
        :class:`.MQTTSnipsApp` object:

        >>> self.publish(*end_session('mySessionId', 'myText'))

        This is equivalent to the much more wordy:

        >>> self.publish('hermes/dialogueManager/endSession',
                         {'sessionId': 'mySessionId',
                          'text': 'myText'})

        .. versionadded:: 0.5.2
    """
    if text:
        payload = {'sessionId': session_id, 'text': text}
    else:
        payload = {'sessionId': session_id}

    return (DM_END_SESSION, payload)
