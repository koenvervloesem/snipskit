"""This module gives a way to access the configuration of a locally installed
instance of Snips, a Snips assistant and a Snips skill.

Classes:
    :class:`AppConfig`: Gives access to the configuration of a Snips app.

    :class:`AssistantConfig`: Gives access to the configuration of a Snips
        assistant.

    :class:`SnipsConfig`: Gives access to the configuration of a locally
        installed instance of Snips.

"""

from collections import UserDict
from configparser import ConfigParser
import json
from pathlib import Path

from hermes_python.ontology import MqttOptions
from snipskit.exceptions import AssistantConfigNotFoundError, SnipsConfigNotFoundError
from snipskit.tools import find_path
import toml

SEARCH_PATH_SNIPS = ['/etc/snips.toml', '/usr/local/etc/snips.toml']
SEARCH_PATH_ASSISTANT = ['/usr/share/snips/assistant/assistant.json',
                         '/usr/local/share/snips/assistant/assistant.json']
DEFAULT_BROKER = 'localhost:1883'


class AppConfig(ConfigParser):
    """
    This class gives access to the configuration of a Snips app as a
    ConfigParser object.

    Attributes:
        filename (str): The filename of the configuration file.

    Example:
        >>> config = AppConfig()  # Use default file config.ini
        >>> config['secret']['api-key']
        'foobar'
        >>> config['secret']['api-key'] = 'barfoo'
        >>> config.write()
    """

    def __init__(self, filename=None):
        """Initialize an :class:`AppConfig` object.

        Args:
            filename (optional): A filename for the configuration file. If the
                filename is not specified, the default filename 'config.ini'
                is chosen.
        """

        ConfigParser.__init__(self)

        if not filename:
            filename = 'config.ini'

        self.filename = filename

        config_path = Path(filename)

        with config_path.open('rt') as config:
            self.read_file(config)

    def write(self, *args, **kwargs):
        """Write the current configuration to the app's configuration file.

        If this method is called without any arguments, the configuration is
        written to the `filename` attribute of this object.

        If this method is called with any arguments, they are forwarded to the
        `write` method of the superclass `ConfigParser`.
        """
        if len(args) + len(kwargs):
            super().write(*args, **kwargs)
        else:
            with Path(self.filename).open('wt') as config:
                super().write(config)


class AssistantConfig(UserDict):
    """
    This class gives access to the configuration of a Snips assistant as a
     dict.

    Attributes:
        filename (str): The filename of the configuration file.

    Example:
        >>> assistant = AssistantConfig('/opt/assistant/assistant.json')
        >>> assistant['language']
        'en'
    """

    def __init__(self, filename=None):
        """Initialize an :class:`AssistantConfig` object.

        Args:
            filename (:obj:`str`, optional): The path of the assistant's
                configuration file.

                If the argument is not specified, the configuration file is
                searched for in the following locations, in this order:

                - /usr/share/snips/assistant/assistant.json
                - /usr/local/share/snips/assistant/assistant.json

        Raises:
            FileNotFoundError: If the specified filename doesn't exist.

            AssistantConfigNotFoundError: If there's no assistant
                configuration found in the search path.

            JSONDecodeError: If the assistant's configuration file
                doesn't have a valid JSON syntax.

        Examples:
            >>> assistant = AssistantConfig()  # default configuration
            >>> assistant2 = AssistantConfig('/opt/assistant/assistant.json')
        """
        if filename:
            self.filename = filename
            assistant_file = Path(filename)
        else:
            self.filename = find_path(SEARCH_PATH_ASSISTANT)

            if not self.filename:
                raise AssistantConfigNotFoundError()

            assistant_file = Path(self.filename)

        # Open the assistant's file. This raises FileNotFoundError if the
        # file doesn't exist.
        with assistant_file.open('rt') as json_file:
            # Create a dict with our configuration.
            # This raises JSONDecodeError if the file doesn't have a
            # valid JSON syntax.
            UserDict.__init__(self, json.load(json_file))


class SnipsConfig(UserDict):
    """This class gives access to a snips.toml configuration file as a dict.

    Attributes:
        filename (str): The filename of the configuration file.
        mqtt (:obj:`MqttOptions`): The MQTT options of the Snips configuration.

    Example:
        >>> snips = SnipsConfig()
        >>> snips['snips-hotword']['audio']
        ['default@mqtt', 'bedroom@mqtt']
    """

    def __init__(self, filename=None):
        """Initialize a :class:`SnipsConfig` object.

        The `mqtt` attribute is initialized with the MQTT connection settings
            from the configuration file, or the default value 'localhost:1883'
            for the broker address if the settings are not specified.

        Args:
            filename (`str`, optional): The full path of the config file. If
                the argument is not specified, the file snips.toml is searched
                for in the following locations, in this order:

                - /etc/snips.toml
                - /usr/local/etc/snips.toml

        Raises:
            FileNotFoundError: If `filename` is specified but doesn't exist.

            SnipsConfigNotFoundError: If there's no snips.toml found in the
                search path.

            TomlDecodeError: If `filename` doesn't have a valid TOML syntax.

        Examples:
            >>> snips = SnipsConfig()  # Tries to find snips.toml.
            >>> snips_local = SnipsConfig('/usr/local/etc/snips.toml')
        """
        if filename:
            if not Path(filename).is_file():
                raise FileNotFoundError('{} not found'.format(filename))
            self.filename = filename
        else:
            self.filename = find_path(SEARCH_PATH_SNIPS)
            if not self.filename:
                raise SnipsConfigNotFoundError()

        # Create a dict with our configuration.
        # This raises TomlDecodeError if the file doesn't have a valid TOML
        # syntax.
        UserDict.__init__(self, toml.load(self.filename))

        # Now find all the MQTT options in the configuration file and use
        # sensible defaults for options that aren't specified.
        try:
            # Basic MQTT connection settings.
            broker_address = self['snips-common'].get('mqtt', DEFAULT_BROKER)

            # MQTT authentication
            username = self['snips-common'].get('mqtt_username', None)
            password = self['snips-common'].get('mqtt_password', None)

            # MQTT TLS configuration
            tls_hostname = self['snips-common'].get('mqtt_tls_hostname', None)
            tls_ca_file = self['snips-common'].get('mqtt_tls_cafile', None)
            tls_ca_path = self['snips-common'].get('mqtt_tls_capath', None)
            tls_client_key = self['snips-common'].get('mqtt_tls_client_key',
                                                      None)
            tls_client_cert = self['snips-common'].get('mqtt_tls_client_cert',
                                                       None)
            tls_disable_root_store = self['snips-common'].get('mqtt_tls_disable_root_store',
                                                              False)

            # Store the MQTT connection settings in a MqttOptions object.
            self.mqtt = MqttOptions(broker_address, username, password,
                                    tls_hostname, tls_ca_file, tls_ca_path,
                                    tls_client_key, tls_client_cert,
                                    tls_disable_root_store)
        except KeyError:
            # The 'snips-common' section isn't in the configuration file, so we
            # use a sensible default: 'localhost:1883'.
            self.mqtt = MqttOptions()
