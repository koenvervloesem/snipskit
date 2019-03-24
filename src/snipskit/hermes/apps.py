"""This module contains a class to create Snips apps using the Hermes Python
library.

Example:

.. code-block:: python

    from snipskit.hermes.apps import HermesSnipsApp
    from snipskit.hermes.decorators import intent


    class SimpleSnipsApp(HermesSnipsApp):

        def initialize(self):
            print('App initialized')

        @intent('User:ExampleIntent')
        def example_intent(self, hermes, intent_message):
            print('I received intent "User:ExampleIntent"')
"""

from snipskit.apps import SnipsAppMixin
from snipskit.hermes.components import HermesSnipsComponent


class HermesSnipsApp(SnipsAppMixin, HermesSnipsComponent):
    """A Snips app using the Hermes Python library.

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
