"""Integration test for subscribing and publishing to MQTT topic in the
:class:`snipskit.components.MQTTSnipsComponent` class.

This needs mosquitto running on localhost:1883.
"""
import json
import os
import subprocess
import re
import threading
import time

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import pytest

from snipskit.mqtt.components import MQTTSnipsComponent
from snipskit.mqtt.decorators import topic

# Only run these tests if the environment variable INTEGRATION_TESTS is set.
pytestmark = pytest.mark.skipif(not os.environ.get('INTEGRATION_TESTS'),
                                reason='Integration test')
# Delay between subscribing and publishing an MQTT message.
DELAY=0.5

class DecoratedMQTTComponentPubSub(MQTTSnipsComponent):
    """A simple Snips component using MQTT directly to test."""

    @topic('hermes/hotword/+/detected')
    def handle_hotword(self, topic, payload):
        hotword = re.search('^hermes/hotword/(.*)/detected$', topic).group(1)
        siteId = payload['siteId']
        result_sentence = 'I detected the hotword {} on site ID {}.'.format(hotword, siteId)
        self.publish('hermes/tts/say', {'siteId': siteId, 'text': result_sentence})

    @topic('hermes/audioServer/+/playBytes/+', json_decode=False)
    def handle_audio(self, topic, payload):
        parsed_topic = re.search('^hermes/audioServer/(.*)/playBytes/(.*)$', topic)
        siteId = parsed_topic.group(1)
        requestId = parsed_topic.group(2)
        result_sentence = 'I detected audio with request ID {} and payload {} on site ID {}.'.format(requestId, payload.decode('utf-8'), siteId)
        self.publish('hermes/tts/say', {'siteId': siteId, 'text': result_sentence})


def test_snips_component_mqtt_pubsub(mqtt_server):
    """Test whether a :class:`MQTTSnipsComponent` object executes the right
    callback after a topic it's subscribed to gets published on the MQTT bus
    and publishes the right payload.
    """

    def publish_audio():
        publish.single('hermes/audioServer/default/playBytes/1234', 'foobar')

    def publish_hotword():
        publish.single('hermes/hotword/hey_snips/detected', '{"siteId": "default"}')

    # Test handle_hotword method: JSON payload
    threading.Thread(target=DecoratedMQTTComponentPubSub, daemon=True).start()

    threading.Timer(DELAY, publish_hotword).start()

    message = subscribe.simple('hermes/tts/say')
    assert json.loads(message.payload.decode('utf-8')) == {'siteId': 'default',
                                                           'text': 'I detected the hotword hey_snips on site ID default.'}

    # Test handle_audio method: 'Binary' payload (just a string here)
    threading.Timer(DELAY, publish_audio).start()

    message = subscribe.simple('hermes/tts/say')
    assert json.loads(message.payload.decode('utf-8')) == {'siteId': 'default',
                                                           'text': 'I detected audio with request ID 1234 and payload foobar on site ID default.'}
