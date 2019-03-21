"""This module contains classes to create components communicating with Snips.

A Snips component (a subclass of :class:`.SnipsComponent`) can communicate with
Snips services. There are two subclasses of :class:`.SnipsComponent`:

- :class:`.HermesSnipsComponent`: a Snips component using the Hermes protocol;
- :class:`.MQTTSnipsComponent`: a Snips component using the MQTT protocol
  directly.

.. note::
   If you want to create a Snips app with access to an assistant's
   configuration and a configuration for the app, you need to instantiate a
   :class:`.HermesSnipsApp` or :class:`.MQTTSnipsApp` object, which is a
   subclass of :class:`.HermesSnipsComponent` or :class:`.MQTTSnipsComponent`,
   respectively and adds `assistant` and `config` attributes.

Example:

.. code-block:: python

    from snipskit.components import MQTTSnipsComponent
    from snipskit.decorators.mqtt import topic

    class SimpleSnipsComponent(MQTTSnipsComponent):

        def initialize(self):
            print('Component initialized')

        @topic('hermes/hotword/toggleOn')
        def hotword_on(self, client, userdata, msg):
            print('Hotword activated')
"""

from abc import ABCMeta, abstractmethod

from hermes_python.hermes import Hermes
from paho.mqtt.client import Client
from snipskit.config import SnipsConfig


class SnipsComponent(metaclass=ABCMeta):
    """Connect with a Snips instance and give access to a Snips configuration.

    This is an `abstract base class`_. You don't instantiate an object of this
    class, but an object of one of its subclasses:
    :class:`.HermesSnipsComponent` or :class:`.MQTTSnipsComponent`

    .. _`abstract base class`: https://docs.python.org/3/glossary.html#term-abstract-base-class

    Attributes:
        snips (:class:`.SnipsConfig`): The Snips configuration.
    """

    def __init__(self, snips=None):
        """Initialize a Snips component.

        Args:
            snips (:class:`.SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default
                :class:`.SnipsConfig` object is created for a locally installed
                instance of Snips.
        """
        if not snips:
            snips = SnipsConfig()
        self.snips = snips

        self._connect()
        self.initialize()
        self._start()

    @abstractmethod
    def _connect(self):
        """Connect with Snips.

        This method should be implemented in a subclass of
        :class:`.SnipsComponent`.
        """
        pass

    def initialize(self):
        """If you have to initialize a component in your subclass of
        :class:`.SnipsComponent`, add your code in this method. It will be
        called between connecting to Snips and starting the event loop.
        """
        pass

    @abstractmethod
    def _start(self):
        """Connect with Snips.

        This method should be implemented in a subclass of
        :class:`.SnipsComponent`.
        """
        pass


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

    def _subscribe_topics(self, client, userdata, flags, rc):
        """Subscribe to the MQTT topics we're interested in.

        Each method with an attribute set by a @topic decorator is registered
        as a callback for the corresponding topic.
        """
        for name in dir(self):
            callable_name = getattr(self, name)
            if hasattr(callable_name, 'topic'):
                self.mqtt.subscribe(getattr(callable_name, 'topic'))
                self.mqtt.message_callback_add(getattr(callable_name, 'topic'),
                                               callable_name)


class HermesSnipsComponent(SnipsComponent):
    """A Snips component using the Hermes protocol.

    Attributes:
        snips (:class:`.SnipsConfig`): The Snips configuration.
        hermes (:class:`hermes_python.hermes.Hermes`): The Hermes object.

    """

    def _connect(self):
        """Connect with the MQTT broker referenced in the snips configuration
        file.
        """
        self.hermes = Hermes(mqtt_options=self.snips.mqtt)
        self.hermes.connect()
        self._register_callbacks()

    def _start(self):
        """Start the event loop to the Hermes object so the component
        starts listening to events and the callback methods are called.
        """
        self.hermes.loop_forever()

    def _register_callbacks(self):
        """Subscribe to the Hermes events we're interested in.

        Each method with an attribute set by a decorator is registered as a
        callback for the corresponding event.
        """
        for name in dir(self):
            callable_name = getattr(self, name)

            if hasattr(callable_name, 'intent'):
                self.hermes.subscribe_intent(getattr(callable_name, 'intent'),
                                             callable_name)
            self._check_callback(callable_name, 'intent_not_recognized')
            self._check_callback(callable_name, 'intents')
            self._check_callback(callable_name, 'session_ended')
            self._check_callback(callable_name, 'session_queued')
            self._check_callback(callable_name, 'session_started')

    def _check_callback(self, method, event):
        """Check if method `method` has an attribute `event`. If it has,
        call the right subscribe method of our Hermes object to register the
        method as a callback.
        """
        if hasattr(method, event):
            getattr(self.hermes, 'subscribe_' + event)(method)
