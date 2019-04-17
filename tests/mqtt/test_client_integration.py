"""Integration test for the :mod:`snipskit.mqtt.client` module.

This needs mosquitto running on localhost:1883.
"""
import json
import os
import subprocess
import re
import threading
import time

import paho.mqtt.subscribe as subscribe
import pytest

from snipskit.config import MQTTConfig
from snipskit.mqtt.client import publish_single

# Only run these tests if the environment variable INTEGRATION_TESTS is set.
pytestmark = pytest.mark.skipif(not os.environ.get('INTEGRATION_TESTS'),
                                reason='Integration test')
# Delay between subscribing and publishing an MQTT message.
DELAY=1


def test_client_publish_single(mqtt_server):

    config = MQTTConfig()

    def publish_test():
        publish_single(config, 'snipskit-test/topic', 'foobar')

    threading.Timer(DELAY, publish_test).start()

    message = subscribe.simple('snipskit-test/topic')
    assert message.payload.decode('utf-8') == 'foobar'
