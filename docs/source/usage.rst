#####
Usage
#####

The design philosophy of SnipsKit is:

- It should be easy to create a Snips app with minimal `boilerplate code`_.
- All SnipsKit code should behave by default in a sensible way, tuned for a Snips installation.

.. _`boilerplate code`: https://en.wikipedia.org/wiki/Boilerplate_code

*************
Prerequisites
*************

This document presupposes that you:

- know Python, in particular `Python 3`_;
- have Snips running and have read the `Snips Platform documentation`_;
- know how to interface with the Snips platform using `Hermes Python`_ or MQTT_.

.. _Python: https://www.python.org/

.. _`Python 3`: https://docs.python.org/3/tutorial/

.. _`Snips Platform documentation`: https://docs.snips.ai/

.. _`Hermes Python`: https://docs.snips.ai/articles/console/actions/actions/code-your-action/hermes-python

.. _MQTT: https://docs.snips.ai/reference/hermes

***************************************
Creating Snips apps using Hermes Python
***************************************

You can create a Snips app using Hermes Python by subclassing the :class:`.HermesSnipsApp` class. This is a convenience class that removes a lot of boilerplate code, which it executes behind the curtains without you having to think about it.

But you still have to know how to use the Hermes Python library, because you'll use it to read slots, publish messages, and so on. Think of the :class:`.HermesSnipsApp` class as an addon that makes your life in the Hermes Python world a little easier.

Creating a simple Snips app using Hermes Python
===============================================

A simple Snips app that listens to a specific intent and then says a message, is created like this:

.. literalinclude :: ../../examples/hermes_listen_for_intent.py
   :language: python
   :linenos:
   :start-at: from snipskit.apps
   :append: #!/usr/bin/env/python3
