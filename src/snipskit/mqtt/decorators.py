"""This module contains decorators_ to apply to methods of a
:class:`.MQTTSnipsComponent` object.

.. _decorators: https://docs.python.org/3/glossary.html#term-decorator

By applying one of these decorators to a method of a
:class:`.MQTTSnipsComponent` object, this method is registered as a callback to
the corresponding event. When the event fires (e.g. an MQTT topic is
published), the method is called.

Example:

.. code-block:: python

    from snipskit.mqtt.apps import MQTTSnipsApp
    from snipskit.mqtt.decorators import topic

    class SimpleSnipsApp(MQTTSnipsApp):

        @topic('hermes/hotword/toggleOn')
        def hotword_on(self, topic, payload):
            print('Hotword on {} is toggled on.'.format(payload['siteId']))
"""

import json


def topic(topic_name, json_decode=True):
    """Apply this decorator to a method of class :class:`.MQTTSnipsComponent`
    to register it as a callback to be triggered when the MQTT topic
    `topic_name` is published.

    The callback needs to have the following signature:

    method(self, topic, payload)

    Args:
        topic_name (str): The MQTT topic you want to subscribe to.
        json_decode (bool, optional): Whether or not the payload will be
            decoded as JSON to a dict. The default value is True. Set this to
            False if you want to subscribe to a topic with a binary payload.
    """
    def wrapper(method):
        def wrapped(self, client, userdata, msg):
            """This is the callback with the signature that Paho MQTT expects.
            """
            if json_decode:
                payload = json.loads(msg.payload.decode('utf-8'))
            else:
                payload = msg.payload

            # This is the callback with the signature that SnipsKit expects.
            method(self, msg.topic, payload)

        wrapped.topic = topic_name
        return wrapped
    return wrapper
