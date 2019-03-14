"""This module contains classes to create Snips apps.

Classes:
    MQTTSnipsApp: A Snips app using MQTT directly.
    HermesSnipsApp: A Snips app using the Hermes protocol.

"""

from snipskit.components import HermesSnipsComponent, MQTTSnipsComponent
from snipskit.config import AssistantConfig


class MQTTSnipsApp(MQTTSnipsComponent):
    """A Snips app using the MQTT protocol directly.

    Attributes:
        assistant (:obj:`AssistantConfig`): The assistant configuration.
        config (:obj:`AppConfig`): The app configuration.
        snips (:obj:`SnipsConfig`): The Snips configuration.
        mqtt (:obj:`paho.mqtt.client.Client`): The MQTT client object.
    """

    def __init__(self, snips=None, assistant=None, config=None):
        """Initialize a Snips app using the MQTT protocol.

        Args:
            snips (:obj:`SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default :obj:`SnipsConfig`
                object is created for a locally installed instance of Snips.

            assistant (:obj:`AssistantConfig`, optional): an assistant
                configuration. If the argument is not specified, a default
               :obj:`AssistantConfig` object is created.

            config (:obj:`AppConfig`, optional): an app configuration. If the
                argument is not specified, the app has no configuration.

        """
        self.config = config

        if not assistant:
            assistant = AssistantConfig(snips)
        self.assistant = assistant

        MQTTSnipsComponent.__init__(self, snips)


class HermesSnipsApp(HermesSnipsComponent):
    """A Snips app using the Hermes protocol.

    Attributes:
        assistant (:obj:`AssistantConfig`): The assistant configuration.
        config (:obj:`AppConfig`): The app configuration.
        snips (:obj:`SnipsConfig`): The Snips configuration.
        hermes (:obj:`hermes_python.hermes.Hermes`): The Hermes object.
    """

    def __init__(self, snips=None, assistant=None, config=None):
        """Initialize a Snips app using the Hermes protocol.

        Args:
            snips (:obj:`SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default :obj:`SnipsConfig`
                object is created for a locally installed instance of Snips.

            assistant (:obj:`AssistantConfig`, optional): an assistant
                configuration. If the argument is not specified, a default
               :obj:`AssistantConfig` object is created.

            config (:obj:`AppConfig`, optional): an app configuration. If the
                argument is not specified, the app has no configuration.

        """
        self.config = config

        if not assistant:
            assistant = AssistantConfig(snips)
        self.assistant = assistant

        HermesSnipsComponent.__init__(self, snips)
