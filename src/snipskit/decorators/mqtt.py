"""This module contains decorators_ to apply to methods of a
:class:`.MQTTSnipsComponent` object.

.. _decorators: https://docs.python.org/3/glossary.html#term-decorator

By applying one of these decorators to a method of a
:class:`.MQTTSnipsComponent` object, this method is registered as a callback to
the corresponding event. When the event fires (e.g. an MQTT topic is
published), the method is called.

Example:

.. code-block:: python

    from snipskit.apps import MQTTSnipsApp
    from snipskit.decorators.mqtt import intent

    class SimpleSnipsApp(MQTTSnipsApp):

        @topic('hermes/hotword/toggleOn')
        def hotword_on(self, client, userdata, msg):
            print('Hotword on')
"""


def topic(topic_name):
    """Apply this decorator to a method of class :class:`.MQTTSnipsComponent`
    to register it as a callback to be triggered when the MQTT topic
    `topic_name` is published.

    Args:
        topic_name (str): The MQTT topic you want to subscribe to.
    """
    def inner(method):
        """The method to apply the decorator to."""
        method.topic = topic_name
        return method
    return inner
