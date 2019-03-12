"""This module contains classes to create Snips apps.

Classes:
    SnipsApp: The base class for all kinds of Snips apps.

    MQTTSnipsApp: A Snips app using MQTT directly.

    HermesSnipsApp: A Snips app using the Hermes protocol.

"""

from collections import UserDict

from hermes_python.ontology import MqttOptions
from hermes_python.hermes import Hermes
from paho.mqtt.client import Client
from snipskit.config import AppConfig, AssistantConfig


class SnipsApp:
    """This class givess access to objects a Snips app needs, such as the
    configuration of the locally installed instance of Snips, the installed
    assistant and the app itself.

    Attributes:
        config (:obj:`AppConfig`): The app configuration.
        assistant (:obj:`AssistantConfig`): The assistant configuration.
    """

    def __init__(self, config=None, assistant=None):
        """Initialize a Snips app.

        Args:
            config (:obj:`AppConfig`, optional): an app configuration. If the
                argument is not specified, the app has no configuration. 

            assistant (:obj:`AssistantConfig`, optional): an assistant
                configuration. If the argument is not specified, a default
                :obj:`AssistantConfig` object is created.
        """

        if not assistant:
            assistant = AssistantConfig()
        self.assistant = assistant


    def initialize(self):
        """If you have to initialize an app in your subclass of
        :obj:'SnipsApp`, add your code in this method and not in `__init__`.
        """
        pass


class MQTTSnipsApp(SnipsApp):
    """A Snips app using the MQTT protocol directly."""

    def __init__(self, config=None, assistant=None):
        """Initialize a Snips app using the MQTT protocol."""
        SnipsApp.__init__(self, config, assistant)

        self.mqtt = Client()
        self.mqtt.on_connect = self._subscribe_topics

        mqtt_options=self.assistant.snips.mqtt
        host_port = mqtt_options.broker_address.split(':')

        # Set up MQTT authentication
        if mqtt_options.username and mqtt_options.password:
            # The parameters mqtt_username and mqtt_password are both specified
            # in snips.toml, so we use them for authentication.
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

        self.initialize()

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


class HermesSnipsApp(SnipsApp):
    """A Snips app using the Hermes protocol."""

    def __init__(self, config=None, assistant=None):
        """Initialize a Snips app using the Hermes protocol."""
        SnipsApp.__init__(self, config, assistant)

        # Create the Hermes object and connect.
        self.hermes = Hermes(mqtt_options=self.assistant.snips.mqtt)
        self.hermes.connect()

        self._register_callbacks()
        self.initialize()

        self.hermes.loop_forever()


    def _register_callbacks(self):
        """Subscribe to the Hermes events we're interested in.

        Each method with an attribute set by a decorator is registered as a
        callback for the corresponding event.
        """
        for name in dir(self):
            callable_name = getattr(self, name)

            if hasattr(callable_name, 'intent'):
                self.hermes.subscribe_intent(getattr(callable_name, 'intent'), callable_name)
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

