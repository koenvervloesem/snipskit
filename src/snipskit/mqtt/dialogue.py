"""This module contains some helper functions to work with MQTT messages using
the `Snips dialogue API`_.

.. _`Snips dialogue API`: https://docs.snips.ai/reference/dialogue
"""

DM_END_SESSION = 'hermes/dialogueManager/endSession'

def end_session(session_id, text):
    """Return a tuple with a topic and payload for an endSession message for
    the specified session ID and text.

    Args:
        session_id (str): The session Id of the message.
        text (str): The text to say before ending the session.

    Returns:
        (str, dict): A tuple of the topic and the payload to call
            :meth:`.MQTTSnipsComponent.publish` with.

    Example:
        You would use this function like this in a callback method of an
        :class:`.MQTTSnipsApp` object:

        >>>> self.publish(*end_session('mySessionId', 'myText'))

        This is equivalent to the much more wordy:

        >>>> self.publish('hermes/dialogueManager/endSession',
                          {'sessionId': 'mySessionId',
                           'text': 'myText'})
    """
    return (DM_END_SESSION,  # Topic
            {'sessionId': session_id, 'text': text})  # Payload
