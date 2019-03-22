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
    """A `mixin`_ for classes that should have access to a Snips app's
    configuration, the Snips assistant's configuration and the Snips
    configuration.

    The classes :class:`.HermesSnipsApp` and :class:`.MQTTSnipsApp` include
    this mixin, primarily to avoid code duplication for reading the assistant's
    configuration from the location defined in snips.toml.

    You can also subclass this mixin for easy access to the Snips configuration
    and the assistant's configuration without the need to connect to the MQTT
    broker.

    Attributes:
        assistant (:class:`.AssistantConfig`): The assistant configuration. Its
            location is read from the Snips configuration file.
        config (:class:`.AppConfig`): The app configuration.
        snips (:class:`.SnipsConfig`): The Snips configuration.

    .. _`mixin`: https://en.wikipedia.org/wiki/Mixin
    """

    def __init__(self, snips=None, config=None):
        """Initialize the mixin by setting the :attr:`config`, :attr:`snips`
        and :attr:`assistant` attributes.

        To initialize the :attr:`assistant` attribute, the location of the
        assistant is read from the Snips configuration file. If the location is
        not specified there, a default :class:`.AssistantConfig` object is
        created.

        Args:
            snips (:class:`.SnipsConfig`, optional): a Snips configuration.
                If the argument is not specified, a default
                :class:`.SnipsConfig` object is created for a locally installed
                instance of Snips.

            config (:class:`.AppConfig`, optional): an app configuration. If
                the argument is not specified, the app has no configuration.

        .. versionadded:: 0.3.0
        """
        self.config = config

        if not snips:
            snips = SnipsConfig()
        self.snips = snips

        try:
            assistant_directory = snips['snips-common']['assistant']
            assistant_file = Path(assistant_directory) / 'assistant.json'
            self.assistant = AssistantConfig(assistant_file)
        except KeyError:
            self.assistant = AssistantConfig()


class MQTTSnipsApp(SnipsAppMixin, MQTTSnipsComponent):
    """A Snips app using the MQTT protocol directly.

    Attributes:
        assistant (:class:`.AssistantConfig`): The assistant configuration. Its
            location is read from the Snips configuration file and otherwise a
            default location is used.
        config (:class:`.AppConfig`): The app configuration.
        snips (:class:`.SnipsConfig`): The Snips configuration.
        mqtt (`paho.mqtt.client.Client`_): The MQTT client object.

    .. _`paho.mqtt.client.Client`: https://www.eclipse.org/paho/clients/python/docs/#client

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
        SnipsAppMixin.__init__(self, snips, config)
        MQTTSnipsComponent.__init__(self, snips)


class HermesSnipsApp(SnipsAppMixin, HermesSnipsComponent):
    """A Snips app using the Hermes protocol.

    Attributes:
        assistant (:class:`.AssistantConfig`): The assistant configuration. Its
            location is read from the Snips configuration file and otherwise
            a default location is used.
        config (:class:`.AppConfig`): The app configuration.
        snips (:class:`.SnipsConfig`): The Snips configuration.
        hermes (:class:`hermes_python.hermes.Hermes`): The Hermes object.

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
        SnipsAppMixin.__init__(self, snips, config)
        HermesSnipsComponent.__init__(self, snips)
