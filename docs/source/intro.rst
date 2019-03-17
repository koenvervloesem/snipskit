SnipsKit is a Python library with some helper tools to work with the voice assistant Snips_. This can be used by Snips apps or other programs that work with Snips.

.. _Snips: https://snips.ai/

With SnipsKit, you can create Snips apps without having to write much boilerplate code. The simplest example of an app using SnipsKit is the following:

.. code-block:: python

    from snipskit.apps import HermesSnipsApp
    from snipskit.decorators import intent

    class SimpleSnipsApp(HermesSnipsApp):

        @intent('User:ExampleIntent')
        def example_intent(self, hermes, intent_message):
            hermes.publish_end_session(intent_message.session_id, "I received ExampleIntent")

    if __name__ == "__main__":
        SimpleSnipsApp()

And that's it! No need to connect to an MQTT broker, no need to register callbacks, because the HermesSnipsApp class:

- reads the MQTT connection settings from the snips.toml file;
- connects to the MQTT broker;
- registers the method with the @intent decorator as a callback method for the intent 'User:ExampleIntent';
- starts the event loop.

SnipsKit also has decorators for other events, and there's also a class MQTTSnipsApp to listen to MQTT topics directly. Moreover, SnipsKit also gives the app easy access to:

- the Snips configuration;
- the Hermes or MQTT connection object;
- the assistant's configuration;
- the app's configuration.
