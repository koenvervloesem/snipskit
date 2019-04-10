"""Integration tests for the `snipskit.services` module.

This needs snips-dialogue and snips-nlu running, as well as mosquitto listening
on localhost:1883.
"""
import os
import subprocess
import time

import pytest

from snipskit.services import _version_output, is_installed, is_running, \
    model_version, installed, running, versions, version

# Only run these tests if the environment variable INTEGRATION_TESTS is set.
pytestmark = pytest.mark.skipif(not os.environ.get('INTEGRATION_TESTS'),
                                reason='Integration test')

@pytest.fixture
def snips_tts(mqtt_server):
    print('Starting Snips TTS')
    snips_tts = subprocess.Popen('snips-tts')
    time.sleep(1)  # Let's wait a bit before it's started
    yield snips_tts
    print('Tearing down Snips TTS')
    snips_tts.kill()

def test_version_output():
    """Test whether the `_version_output` function returns the right result."""

    # These services are installed
    assert _version_output('snips-dialogue') == 'snips-dialogue 1.1.2 (0.62.3)'
    assert _version_output('snips-nlu') == 'snips-nlu 1.1.2 (0.62.3) [model_version: 0.19.0]'
    assert _version_output('snips-tts') == 'snips-tts 1.1.2 (0.62.3)'

    # These services are not installed
    assert _version_output('snips-asr') == ''
    assert _version_output('snips-audio-server') == ''

def test_is_installed():
    """Test whether the `is_installed` function returns the right result."""

    # These services are installed
    assert is_installed('snips-dialogue')
    assert is_installed('snips-nlu')
    assert is_installed('snips-tts')

    # These services are not installed
    assert not is_installed('snips-asr')
    assert not is_installed('snips-audio-server')

def test_is_running(snips_tts):
    """Test whether the `is_running` function returns the right result."""

    # This service is running 
    assert is_running('snips-tts')

    # These services are not running 
    assert not is_running('snips-asr')
    assert not is_running('snips-audio-server')
    assert not is_running('snips-dialogue')
    assert not is_running('snips-nlu')

def test_model_version():
    """Test whether the `model_version` function returns the right result."""

    assert model_version() == '0.19.0'

def test_installed():
    """test whether the `installed` function returns the right result.
    """
    assert installed() == {'snips-analytics': False,
                           'snips-asr': False,
                           'snips-asr-google': False,
                           'snips-audio-server': False,
                           'snips-dialogue': True,
                           'snips-hotword': False,
                           'snips-injection': False,
                           'snips-nlu': True,
                           'snips-skill-server': False,
                           'snips-tts': True}

def test_running(snips_tts):
    """Test whether the `running` function returns the right result.
    """
    assert running() == {'snips-analytics': False,
                         'snips-asr': False,
                         'snips-asr-google': False,
                         'snips-audio-server': False,
                         'snips-dialogue': False,
                         'snips-hotword': False,
                         'snips-injection': False,
                         'snips-nlu': False,
                         'snips-skill-server': False,
                         'snips-tts': True}

def test_versions():
    """test whether the `versions` function returns the right result.
    """
    assert versions() == {'snips-analytics': '',
                          'snips-asr': '',
                          'snips-asr-google': '',
                          'snips-audio-server': '',
                          'snips-dialogue': '1.1.2',
                          'snips-hotword': '',
                          'snips-injection': '',
                          'snips-nlu': '1.1.2',
                          'snips-skill-server': '',
                          'snips-tts': '1.1.2'}

def test_version():
    """Test whether the `version` function returns the right result."""

    assert version('snips-asr') == ''
    assert version('snips-tts') == '1.1.2'
    assert version() == '1.1.2'

