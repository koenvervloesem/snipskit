"""This module contains a class to create components to communicate with Snips
using the MQTT protocol directly.

.. note::
   If you want to create a Snips app with access to an assistant's
   configuration and a configuration for the app, you need to instantiate a
   :class:`.MQTTSnipsApp` object, which is a subclass of
   :class:`.MQTTSnipsComponent` and adds `assistant` and `config` attributes.

Example:

.. code-block:: python

    from snipskit.mqtt.components import MQTTSnipsComponent

    component = MQTTSnipsComponent()

    @component.topic('hermes/hotword/toggleOn')
    def hotword_on(topic, payload):
        print('Hotword on site {} is toggled on.'.format(payload['siteId']))

    if __name__ == '__main__':
        component.run()
"""
import json

from paho.mqtt.client import Client
from snipskit.components import SnipsComponent
from snipskit.mqtt.client import connect


class MQTTSnipsComponent(SnipsComponent):
    """A Snips component using the MQTT protocol directly.

    Attributes:
        snips (:class:`.SnipsConfig`): The Snips configuration.
        mqtt (`paho.mqtt.client.Client`_): The MQTT client object.

    .. _`paho.mqtt.client.Client`: https://www.eclipse.org/paho/clients/python/docs/#client
    """

    def __init__(self, snips=None):
        """Initialize an :class:`.MQTTSnipsComponent` object.

        Args:
            snips (:class:`.SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default
                :class:`.SnipsConfig` object is created for a locally installed
                instance of Snips.
        """
        SnipsComponent.__init__(self, snips)

        self.mqtt = Client()

        # This will contain a dict of the topic (str) -> callbacks (list)
        # function mappings.
        self._callbacks_topic = {}

    def _connect(self):
        """Connect with the MQTT broker referenced in the Snips configuration
        file.
        """
        self.mqtt.on_connect = self._subscribe_topics
        connect(self.mqtt, self.snips.mqtt)

    def _start(self):
        """Start the event loop to the MQTT broker so the component starts
        listening to MQTT topics and the callback methods are called.
        """
        self.mqtt.loop_forever()

    def _subscribe_topics(self, client, userdata, flags, connection_result):
        """Subscribe to the MQTT topics we're interested in.

        Each function decorated by :meth:`.MQTTSnipsComponent.topic` is
        registered as a callback for the corresponding topic.
        """
        for topic, callbacks in self._callbacks_topic.items():
            self.mqtt.subscribe(topic)
            for callback in callbacks:
                self.mqtt.message_callback_add(topic, callback)

    def publish(self, topic, payload, json_encode=True):
        """Publish a payload on an MQTT topic on the MQTT broker of this
        object.

        Args:
            topic (str): The MQTT topic to publish the payload on.
            payload (str): The payload to publish.
            json_encode (bool, optional): Whether or not the payload is a dict
                that will be encoded as a JSON string. The default value is
                True. Set this to False if you want to publish a binary payload
                as-is.

        Returns:
            :class:`paho.mqtt.MQTTMessageInfo`: Information about the
            publication of the message.

        .. versionadded:: 0.5.0
        """
        if json_encode:
            payload = json.dumps(payload)

        return self.mqtt.publish(topic, payload)

    def topic(self, topic_name, json_decode=True):
        """Apply this decorator to a function to register it as a callback to
        be triggered when the MQTT topic `topic_name` is published.

        The callback needs to have the following signature:

        function(topic, payload)

        Args:
            topic_name (str): The MQTT topic you want to subscribe to.
            json_decode (bool, optional): Whether or not the payload will be
                decoded as JSON to a dict. The default value is True. Set this
                to False if you want to subscribe to a topic with a binary
                payload.
        
        .. versionadded:: 0.7.0
        """
        def wrapper(function):
            def wrapped(client, userdata, msg):
                """This is the callback with the signature that Paho MQTT
                   expects.
                """
                if json_decode:
                    payload = json.loads(msg.payload.decode('utf-8'))
                else:
                    payload = msg.payload

                # This is the callback with the signature that SnipsKit
                # expects.
                function(msg.topic, payload)

            try:
                self._callbacks_topic[topic_name].append(wrapped)
            except KeyError:
                self._callbacks_topic[topic_name] = [wrapped]

            return wrapped
        return wrapper
