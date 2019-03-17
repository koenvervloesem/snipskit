"""This module contains classes to create Snips apps.

You can create a Snips app in two ways:

- By subclassing :class:`.HermesSnipsApp`: This creates a Snips app using the
  Hermes protocol.
- By subclassing :class:`.MQTTSnipsApp`: This creates a Snips app using the
  MQTT protocol directly.

:class:`.HermesSnipsApp` is a subclass of :class:`.HermesSnipsComponent` and
adds `assistant` and `config` attributes for access to the assistant's
configuration and the app's configuration, respectively.

:class:`.MQTTSnipsApp` is a subclass of :class:`.MQTTSnipsComponent` and adds
`assistant` and `config` attributes for access to the assistant's configuration
and the app's configuration, respectively.

Both classes of this module include the :class:`.SnipsAppMixin` mixin to read
the assistant's configuration from the location defined in snips.toml.
"""

from pathlib import Path

from snipskit.components import HermesSnipsComponent, MQTTSnipsComponent
from snipskit.config import AssistantConfig, SnipsConfig


class SnipsAppMixin:
    """A `mixin`_ for classes that should have access to a Snips assistant's
    configuration.

    The classes :class:`.HermesSnipsApp` and :class:`.MQTTSnipsApp` include
    this mixin to avoid code duplication for reading the assistant's
    configuration from the location defined in snips.toml.

    .. _`mixin`: https://en.wikipedia.org/wiki/Mixin
    """

    def get_assistant(self, snips):
        """ Read the assistant configuration. Its location is read from the
        Snips configuration file. If the location is not specified there, a
        default :class:`.AssistantConfig` object is returned.

        Args:
            snips (:class:`.SnipsConfig`): The Snips configuration file that
                has the location of the assistant.

        Returns:
            :class:`.AssistantConfig`: The configuration of the assistant
            belonging to the Snips instance.
        """

        try:
            assistant_directory = snips['snips-common']['assistant']
            assistant_file = Path(assistant_directory) / 'assistant.json'
            assistant = AssistantConfig(assistant_file)
        except KeyError:
            assistant = AssistantConfig()

        return assistant


class MQTTSnipsApp(SnipsAppMixin, MQTTSnipsComponent):
    """A Snips app using the MQTT protocol directly.

    Attributes:
        assistant (:class:`.AssistantConfig`): The assistant configuration. Its
            location is read from the Snips configuration file.
        config (:class:`.AppConfig`): The app configuration.
        snips (:class:`.SnipsConfig`): The Snips configuration.
        mqtt (`paho.mqtt.client.Client`_): The MQTT client object.

    .. _`paho.mqtt.client.Client`: https://github.com/eclipse/paho.mqtt.python#client

    """

    def __init__(self, snips=None, config=None):
        """Initialize a Snips app using the MQTT protocol.

        Args:
            snips (:class:`.SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default
                :class:`.SnipsConfig` object is created for a locally installed
                instance of Snips.

            config (:class:`.AppConfig`, optional): an app configuration. If
                the argument is not specified, the app has no configuration.

        """
        self.config = config

        if not snips:
            snips = SnipsConfig()

        self.assistant = self.get_assistant(snips)

        MQTTSnipsComponent.__init__(self, snips)


class HermesSnipsApp(SnipsAppMixin, HermesSnipsComponent):
    """A Snips app using the Hermes protocol.

    Attributes:
        assistant (:class:`.AssistantConfig`): The assistant configuration. Its
            location is read from the Snips configuration file.
        config (:class:`.AppConfig`): The app configuration.
        snips (:class:`.SnipsConfig`): The Snips configuration.
        hermes (`hermes_python.hermes.Hermes`_): The Hermes object.

    .. _`hermes_python.hermes.Hermes`: https://github.com/snipsco/hermes-protocol/tree/develop/platforms/hermes-python

    """

    def __init__(self, snips=None, config=None):
        """Initialize a Snips app using the Hermes protocol.

        Args:
            snips (:class:`.SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default
                :class:`.SnipsConfig` object is created for a locally installed
                instance of Snips.

            config (:class:`.AppConfig`, optional): an app configuration. If
                the argument is not specified, the app has no configuration.

        """
        self.config = config

        if not snips:
            snips = SnipsConfig()

        self.assistant = self.get_assistant(snips)

        HermesSnipsComponent.__init__(self, snips)
