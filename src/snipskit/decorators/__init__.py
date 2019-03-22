"""This module contains decorators_ to apply to methods of a Snips component.

.. _decorators: https://docs.python.org/3/glossary.html#term-decorator

By applying one of these decorators to a method of a :class:`.SnipsComponent`
object, this method is registered as a callback to the corresponding event.
When the event fires (e.g. an intent happens or an MQTT topic is published),
the method is called.

The decorators are divided in two submodules:

- :mod:`snipskit.decorators.hermes`: Decorators you can apply to the methods of
  a :class:`.HermesSnipsComponent` object.
- :mod:`snipskit.decorators.mqtt`: Decorators you can apply to the methods of a
  :class:`.MQTTSnipsComponent` object.
"""
