########
SnipsKit
########

.. image:: https://api.travis-ci.com/koenvervloesem/snipskit.svg?branch=master
   :target: https://travis-ci.com/koenvervloesem/snipskit
   :alt: Build status

.. image:: https://api.codeclimate.com/v1/badges/46806611ac7c0e5c1613/maintainability
   :target: https://codeclimate.com/github/koenvervloesem/snipskit/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/46806611ac7c0e5c1613/test_coverage
   :target: https://codeclimate.com/github/koenvervloesem/snipskit/test_coverage
   :alt: Test coverage

.. image:: https://api.codacy.com/project/badge/Grade/10e65e471a044d2e9ea0b171626a3333
   :target: https://www.codacy.com/app/koenvervloesem/snipskit
   :alt: Code quality

.. image:: https://readthedocs.org/projects/snipskit/badge/?version=latest
   :target: https://snipskit.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status

.. image:: https://img.shields.io/pypi/v/snipskit.svg
   :target: https://pypi.python.org/pypi/snipskit
   :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/snipskit.svg
   :target: https://pypi.python.org/pypi/snipskit
   :alt: Supported Python versions

.. image:: https://img.shields.io/github/license/koenvervloesem/snipskit.svg
   :target: https://github.com/koenvervloesem/snipskit/blob/master/LICENSE
   :alt: License

.. inclusion-marker-start-intro

SnipsKit is a Python library with some helper tools to work with the voice assistant Snips_. This can be used by Snips apps or other programs that work with Snips.

.. _Snips: https://snips.ai/

With SnipsKit, you can create Snips apps without having to write much boilerplate code. The simplest example of an app using SnipsKit is the following:

.. code-block:: python

    from snipskit.hermes.apps import HermesSnipsApp
    from snipskit.hermes.decorators import intent

    class SimpleSnipsApp(HermesSnipsApp):

        @intent('User:ExampleIntent')
        def example_intent(self, hermes, intent_message):
            hermes.publish_end_session(intent_message.session_id,
                                       "I received ExampleIntent")

    if __name__ == "__main__":
        SimpleSnipsApp()

.. end-code-block

And that's it! No need to connect to an MQTT broker, no need to register callbacks, because the HermesSnipsApp class:

- reads the MQTT connection settings from the snips.toml file;
- connects to the MQTT broker;
- registers the method with the intent decorator as a callback method for the intent 'User:ExampleIntent';
- starts the event loop.

SnipsKit also has decorators for other events, and there's also a class MQTTSnipsApp to listen to MQTT topics directly. Moreover, SnipsKit also gives the app easy access to:

- the Snips configuration;
- the Hermes or MQTT connection object;
- the assistant's configuration;
- the app's configuration.

.. warning:: SnipsKit is currently alpha software. Anything may change at any time. The public API should not be considered stable.

.. inclusion-marker-end-intro

*******************
System requirements
*******************

.. inclusion-marker-start-requirements

SnipsKit is a Python 3-only library, requiring Python 3.5 or higher. It's currently tested on Python 3.5, 3.6 and 3.7.

.. inclusion-marker-end-requirements

************
Installation
************

.. inclusion-marker-start-installation

SnipsKit is `packaged on PyPI`_. The latest stable version with all functionality can be installed with the following command:

.. _`packaged on PyPI`: https://pypi.org/project/snipskit/

.. code-block:: sh

    pip install snipskit[hermes,mqtt]

.. inclusion-marker-end-installation

*************
Documentation
*************

The full documentation can be found on Read the Docs, for both the `stable version`_ and the `development version`_.

.. _`stable version`: https://snipskit.readthedocs.io/en/stable/
.. _`development version`: https://snipskit.readthedocs.io/en/latest/

*********
Copyright
*********

This library is provided by `Koen Vervloesem`_ as open source software. See LICENSE_ for more information.

.. _`Koen Vervloesem`: mailto:koen@vervloesem.eu

.. _LICENSE: LICENSE
