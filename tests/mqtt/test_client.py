"""Unit tests for the helper functions of :mod:`snipskit.mqtt.client`.
"""

from snipskit.config import MQTTConfig
from snipskit.mqtt.client import auth_params, host_port, tls_params


# Test auth_params
def test_client_auth_params():
    config = MQTTConfig(username='foo', password='bar')
    auth = auth_params(config)

    assert auth['username'] == 'foo'
    assert auth['password'] == 'bar'


def test_client_auth_params_without_password():
    config = MQTTConfig(username='foo')
    auth = auth_params(config)

    assert auth['username'] == 'foo'
    assert auth['password'] is None


def test_client_auth_params_without_auth():
    config = MQTTConfig()
    auth = auth_params(config)

    assert auth is None


# Test host_port
def test_client_host_port():
    config = MQTTConfig()
    host, port = host_port(config)

    assert host == 'localhost'
    assert port == 1883


def test_client_host_port_tls():
    config = MQTTConfig(tls_hostname='example.com')
    host, port = host_port(config)

    assert host == 'example.com'
    assert port == 1883


# Test tls_params
def test_client_tls_params():
    config = MQTTConfig(tls_hostname='example.com', tls_ca_file='foo',
                        tls_client_key='bar', tls_client_cert='foobar')
    tls = tls_params(config)

    assert tls['ca_certs'] == 'foo'
    assert tls['keyfile'] == 'bar'
    assert tls['certfile'] == 'foobar'


def test_client_tls_params_without_tls():
    config = MQTTConfig()
    tls = tls_params(config)

    assert tls is None

