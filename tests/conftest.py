import os
import subprocess
import sys
import time

import pytest


@pytest.fixture
def mqtt_server():
    print('Starting MQTT server')
    mosquitto = subprocess.Popen('mosquitto')
    time.sleep(1)  # Let's wait a bit before it's started
    yield mosquitto 
    print('Tearing down MQTT server')
    mosquitto.kill()


try:
    # This environment variable is used by Travis CI to define which
    # dependencies are installed. Pytest uses it to define which modules
    # are checked.
    requirements = os.environ['SNIPSKIT_REQUIREMENTS']

    if requirements == 'common':
        collect_ignore = ['mqtt', 'hermes']
    elif requirements == 'mqtt':
        collect_ignore = ['hermes']
    elif requirements == 'hermes':
        collect_ignore = ['mqtt']
    elif requirements == 'all':
    # Run all the tests
        pass
    else:
        sys.exit('Unkown value for SNIPSKIT_REQUIREMENTS environment variable: {}'.format(requirements))
except KeyError:
    # Run all the tests
    pass
