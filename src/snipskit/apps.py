"""This module contains classes to create Snips apps.

Classes:
    MQTTSnipsApp: A Snips app using MQTT directly.
    HermesSnipsApp: A Snips app using the Hermes protocol.

"""

from pathlib import Path

from snipskit.components import HermesSnipsComponent, MQTTSnipsComponent
from snipskit.config import AssistantConfig, SnipsConfig


class MQTTSnipsApp(MQTTSnipsComponent):
    """A Snips app using the MQTT protocol directly.

    Attributes:
        assistant (:obj:`AssistantConfig`): The assistant configuration. Its
            location is read from the Snips configuration file.
        config (:obj:`AppConfig`): The app configuration.
        snips (:obj:`SnipsConfig`): The Snips configuration.
        mqtt (:obj:`paho.mqtt.client.Client`): The MQTT client object.
    """

    def __init__(self, snips=None, config=None):
        """Initialize a Snips app using the MQTT protocol.

        Args:
            snips (:obj:`SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default :obj:`SnipsConfig`
                object is created for a locally installed instance of Snips.

            config (:obj:`AppConfig`, optional): an app configuration. If the
                argument is not specified, the app has no configuration.

        """
        self.config = config

        if not snips:
            snips = SnipsConfig()

        try:
            assistant_directory = snips['snips-common']['assistant']
            assistant_file = Path(assistant_directory) / 'assistant.json'
            self.assistant = AssistantConfig(assistant_file)
        except KeyError:
            self.assistant = AssistantConfig()

        MQTTSnipsComponent.__init__(self, snips)


class HermesSnipsApp(HermesSnipsComponent):
    """A Snips app using the Hermes protocol.

    Attributes:
        assistant (:obj:`AssistantConfig`): The assistant configuration. Its
            location is read from the Snips configuration file.
        config (:obj:`AppConfig`): The app configuration.
        snips (:obj:`SnipsConfig`): The Snips configuration.
        hermes (:obj:`hermes_python.hermes.Hermes`): The Hermes object.
    """

    def __init__(self, snips=None, config=None):
        """Initialize a Snips app using the Hermes protocol.

        Args:
            snips (:obj:`SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default :obj:`SnipsConfig`
                object is created for a locally installed instance of Snips.

            config (:obj:`AppConfig`, optional): an app configuration. If the
                argument is not specified, the app has no configuration.

        """
        self.config = config

        if not snips:
            snips = SnipsConfig()

        try:
            assistant_directory = snips['snips-common']['assistant']
            assistant_file = Path(assistant_directory) / 'assistant.json'
            self.assistant = AssistantConfig(str(assistant_file))
        except KeyError:
            self.assistant = AssistantConfig()

        HermesSnipsComponent.__init__(self, snips)
