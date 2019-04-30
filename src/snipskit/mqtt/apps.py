"""This module contains a class to create Snips apps using the MQTT protocol
directly.
"""

from snipskit.apps import SnipsAppMixin
from snipskit.mqtt.components import MQTTSnipsComponent


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
	
    Example:

	.. code-block:: python

		from snipskit.mqtt.apps import MQTTSnipsApp
		from snipskit.mqtt.dialogue import continue_session

		app = MQTTSnipsApp()

		@app.topic('hermes/intent/name')
		def say_name(topic, payload):
			name = app.assistant['name']
			app.publish(*continue_session(payload['sessionId'], name))

		if __name__ == '__main__':
			app.run()

	.. note::
	If you want to communicate with Snips and don't need access to an
	assistant's nor to a configuration for an app, you can instantiate a
	:class:`.MQTTSnipsComponent` object, which doesn't have `assistant` and
	`config` attributes.
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
