"""This module contains a class to create components to communicate with Snips.

A Snips component (a subclass of :class:`.SnipsComponent`) can communicate with
Snips services. There are two subclasses of :class:`.SnipsComponent` in other
modules:

- :class:`snipskit.hermes.components.HermesSnipsComponent`: a Snips component
  using the Hermes Python library;
- :class:`snipskit.mqtt.components.MQTTSnipsComponent`: a Snips component using
  the MQTT protocol directly.

.. note::
   If you want to create a Snips app with access to an assistant's
   configuration and a configuration for the app, you need to instantiate a
   :class:`.HermesSnipsApp` or :class:`.MQTTSnipsApp` object, which is a
   subclass of :class:`.HermesSnipsComponent` or :class:`.MQTTSnipsComponent`
   respectively, adding `assistant` and `config` attributes. See the module
   :mod:`snipskit.apps`.
"""

from abc import ABCMeta, abstractmethod

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

    def initialize(self):
        """If you have to initialize a component in your subclass of
        :class:`.SnipsComponent`, add your code in this method. It will be
        called between connecting to Snips and starting the event loop.
        """

    @abstractmethod
    def _start(self):
        """Connect with Snips.

        This method should be implemented in a subclass of
        :class:`.SnipsComponent`.
        """
