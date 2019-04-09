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
    from snipskit.mqtt.decorators import topic


    class SimpleSnipsComponent(MQTTSnipsComponent):

        def initialize(self):
            print('Component initialized')

        @topic('hermes/hotword/toggleOn')
        def hotword_on(self, topic, payload):
            print('Hotword on {} is toggled on.'.format(payload['siteId']))
"""
import json

from paho.mqtt.client import Client
from snipskit.components import SnipsComponent


class MQTTSnipsComponent(SnipsComponent):
    """A Snips component using the MQTT protocol directly.

    Attributes:
        snips (:class:`.SnipsConfig`): The Snips configuration.
        mqtt (`paho.mqtt.client.Client`_): The MQTT client object.

    .. _`paho.mqtt.client.Client`: https://www.eclipse.org/paho/clients/python/docs/#client
    """

    def _connect(self):
        """Connect with the MQTT broker referenced in the Snips configuration
        file.
        """
        self.mqtt = Client()
        self.mqtt.on_connect = self._subscribe_topics

        mqtt_options = self.snips.mqtt
        host_port = mqtt_options.broker_address.split(':')

        # Set up MQTT authentication
        if mqtt_options.username and mqtt_options.password:
            # The parameters mqtt_username and mqtt_password are both specified
            # in the Snips configuration, so we use them for authentication.
            self.mqtt.username_pw_set(mqtt_options.username,
                                      mqtt_options.password)

        # Set up an MQTT TLS connection
        if mqtt_options.tls_hostname:


            # Set up TLS.
            self.mqtt.tls_set(ca_certs=mqtt_options.tls_ca_file,
                              certfile=mqtt_options.tls_client_cert,
                              keyfile=mqtt_options.tls_client_key)
            host = mqtt_options.tls_hostname
        else:
            host = host_port[0]

        port = host_port[1]

        self.mqtt.connect(host, int(port), 60)

    def _start(self):
        """Start the event loop to the MQTT broker so the component starts
        listening to MQTT topics and the callback methods are called.
        """
        self.mqtt.loop_forever()

    def _subscribe_topics(self, client, userdata, flags, connection_result):
        """Subscribe to the MQTT topics we're interested in.

        Each method with an attribute set by a
        :func:`snipskit.decorators.mqtt.topic` decorator is registered as a
        callback for the corresponding topic.
        """
        for name in dir(self):
            callable_name = getattr(self, name)
            if hasattr(callable_name, 'topic'):
                self.mqtt.subscribe(getattr(callable_name, 'topic'))
                self.mqtt.message_callback_add(getattr(callable_name, 'topic'),
                                               callable_name)

    def publish(self, topic, payload, json_encode=True):
        """Publish a payload on an MQTT topic on the MQTT broker of this object.

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
