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
- know how to interface with the Snips platform using `Hermes Python`_ or MQTT_ (using `Paho MQTT`_).

.. _Python: https://www.python.org/

.. _`Python 3`: https://docs.python.org/3/tutorial/

.. _`Snips Platform documentation`: https://docs.snips.ai/

.. _`Hermes Python`: https://docs.snips.ai/articles/console/actions/actions/code-your-action/hermes-python

.. _MQTT: https://docs.snips.ai/reference/hermes

.. _`Paho MQTT`: https://www.eclipse.org/paho/clients/python/docs/

***************************************
Creating Snips apps using Hermes Python
***************************************

You can create a Snips app using Hermes Python by subclassing the :class:`.HermesSnipsApp` class. This is a convenience class that removes a lot of boilerplate code, which it executes behind the curtains without you having to think about it.

But you still have to know how to use the Hermes Python library, because you'll use it to read slots, publish messages, and so on. Think of the :class:`.HermesSnipsApp` class as an addon that makes your life in the Hermes Python world a little easier.

Creating a simple Snips app using Hermes Python
===============================================

A simple Snips app that listens to a specific intent and then says a message, is created like this:

.. literalinclude :: ../../examples/hermes_listen_for_intent.py
   :caption: Example hermes_listen_for_intent.py
   :language: python
   :linenos:
   :start-at: from snipskit.hermes.apps
   :prepend: #!/usr/bin/env python3

You can download the file `hermes_listen_for_intent.py`_ from our GitHub repository.

.. _`hermes_listen_for_intent.py`: https://github.com/koenvervloesem/snipskit/blob/master/examples/hermes_listen_for_intent.py

Let's dissect this code. In line 1, we signal to the shell that this file is to be run by the Python 3 interpreter. In lines 2 and 3 we import the :class:`.HermesSnipsApp` class and the :func:`.intent` decorator_ that we use.

.. _decorator: https://docs.python.org/3/glossary.html#term-decorator

Beginning from line 6 we define a class for our Snips App, inheriting from the :class:`.HermesSnipsApp` app. By inheriting from this class, you get a lot of functionality for free, which we'll explain in a minute.

In line 9, we define a `callback method`_. This method will be called when an intent is recognized. Which intent? This is defined by the decorator :func:`.intent` in line 8. So this line says: "If the intent 'User:ExampleIntent' is recognized, call the method `example_intent`.

.. _`callback method`: https://en.wikipedia.org/wiki/Callback_(computer_programming)

Then inside the `example_intent` method, you can use the `hermes` and `intent_message` objects from the Hermes Python library. In this simple case, we end the session by saying a message.

In line 14, we check if the Python file is run on the commandline. If it is, we create a new object of the class we defined. When we initialize this object, it automatically reads the MQTT connection settings from the snips.toml file, connects to the MQTT broker, registers the method with the :func:`.intent` decorator as a callback method for the intent 'User:ExampleIntent' and starts the event loop so the app starts listening to events from the Snips platform.

*************************************************************
Reading the configuration of the app, the assistant and Snips
*************************************************************

Each :class:`.SnipsApp` object has attributes that give the app access to the app's configuration (:class:`.AppConfig`), the assistant's configuration (:class:`.AssistantConfig`) and the configuration of Snips (:class:`.SnipsConfig`). The following example (for :class:`.HermesSnipsApp`, but it works the same for :class:`.MQTTSnipsApp`) shows the use of these three attributes:

.. literalinclude :: ../../examples/hermes_configuration.py
   :caption: Example hermes_configuration.py
   :language: python
   :linenos:
   :start-at: from snipskit.hermes.apps
   :prepend: #!/usr/bin/env python3

You can download the file `hermes_configuration.py`_ from our GitHub repository.

.. _`hermes_configuration.py`: https://github.com/koenvervloesem/snipskit/blob/master/examples/hermes_configuration.py

With `self.config` you get access to this app's configuration as an :class:`.AppConfig` object, which is a subclass of :class:`configparser.ConfigParser`. This example requires you to have a file 'config.ini' in the same directory as the app, with the following content:

.. code-block:: ini

    [global]
    [secret]
    switch=light1

.. note:: To get access to the app configuration, don't forget to add the argument `config=AppConfig()` when initializing your app. If you don't need any app configuration, this argument can be left out.

With `self.assistant` you get access to the assistant's configuration as an :class:`.AssistantConfig` object, which behaves like a :class:`dict`. This reads the configuration from the assistant's directory, which is normally '/usr/share/snips/assistant/assistant.json' on a Raspbian system.

And with `self.snips` you get access to the configuration of Snips, which also behaves like a :class:`dict`. This reads the configuration from the Snips configuration file, which is normally '/etc/snips.toml' on a Raspbian system.

****************************************************
Reading the assistant's configuration outside an app
****************************************************

When you create a :class:`.SnipsApp` object, it reads the location of the assistant from 'snips.toml' and creates an :class:`.AssistantConfig` object with the correct path, which gives you access to the assistant's configuration. See the previous section for an example.

You can also create an :class:`.AssistantConfig` object outside a :class:`.SnipsApp` object, reading its configuration from a specified file:

.. code-block:: python

   assistant = AssistantConfig('/opt/assistant/assistant.json')

The file argument is optional. If you leave it empty, the :class:`.AssistantConfig` object tries to read its configuration from the following files, in this order:

- /usr/share/snips/assistant/assistant.json
- /usr/local/share/snips/assistant/assistant.json

Note that he :class:`.AssistantConfig` object doesn't read its location from 'snips.toml' in this case.

If you want to create an :class:`.AssistantConfig` object outside a :class:`.SnipsApp` object and initialize it from the location specified in 'snips.toml', you need to use :attr:`.SnipsAppMixin().assistant` to get an :class:`.AssistantConfig` object with the correct path.

For instance, this could interesting if you want to know the language of the user's assistant before initializing your app:

.. code-block:: python

   language = SnipsAppMixin().assistant['language']
