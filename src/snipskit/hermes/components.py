"""This module contains a class to create components to communicate with Snips
using the Hermes Python library.

.. note::
   If you want to create a Snips app with access to an assistant's
   configuration and a configuration for the app, you need to instantiate a
   :class:`.HermesSnipsApp` object, which is a subclass of
   :class:`.HermesSnipsComponent` and adds `assistant` and `config` attributes.

Example:

.. code-block:: python

    from snipskit.hermes.components import HermesSnipsComponent
    from snipskit.hermes.decorators import intent


    class SimpleSnipsComponent(HermesSnipsComponent):

        def initialize(self):
            print('Component initialized')

        @intent('User:ExampleIntent')
        def example_intent(self, hermes, intent_message):
            print('I received intent "User:ExampleIntent"')
"""

from hermes_python.hermes import Hermes
from hermes_python.ontology import MqttOptions
from snipskit.components import SnipsComponent


class HermesSnipsComponent(SnipsComponent):
    """A Snips component using the Hermes Python library.

    Attributes:
        snips (:class:`.SnipsConfig`): The Snips configuration.
        hermes (:class:`hermes_python.hermes.Hermes`): The Hermes object.

    """

    def _connect(self):
        """Connect with the MQTT broker referenced in the snips configuration
        file.
        """
        mqtt_options = self.snips.mqtt
        self.hermes = Hermes(mqtt_options=MqttOptions(mqtt_options.broker_address,
                                                      mqtt_options.username,
                                                      mqtt_options.password,
                                                      mqtt_options.tls_hostname,
                                                      mqtt_options.tls_ca_file,
                                                      mqtt_options.tls_ca_path,
                                                      mqtt_options.tls_client_key,
                                                      mqtt_options.tls_client_cert,
                                                      mqtt_options.tls_disable_root_store))
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

            # If we have given the method a subscribe_method attribute by one
            # of the decorators.
            if hasattr(callable_name, 'subscribe_method'):
                subscribe_method = getattr(callable_name, 'subscribe_method')
                # If we have given the method a subscribe_parameter attribute
                # by one of the decorators.
                if hasattr(callable_name, 'subscribe_parameter'):
                    subscribe_parameter = getattr(callable_name,
                                                  'subscribe_parameter')
                    # Register callable_name as a callback with
                    # subscribe_method and subscribe_parameter as a parameter.
                    getattr(self.hermes, subscribe_method)(subscribe_parameter,
                                                           callable_name)
                else:
                    # Register callable_name as a callback with
                    # subscribe_method.
                    getattr(self.hermes, subscribe_method)(callable_name)
