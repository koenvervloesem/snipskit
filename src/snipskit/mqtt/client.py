"""This module contains helper functions to use the MQTT protocol with the MQTT
broker defined in a :class:`.MQTTConfig` object.
"""
from paho.mqtt.client import MQTTv311
from paho.mqtt.publish import single


def auth_params(mqtt_config):
    """Return the authentication parameters from a :class:`.MQTTConfig`
    object.

    Args:
        mqtt_config (:class:`.MQTTConfig`): The MQTT connection settings.

    Returns:
        dict: A dict {'username': username, 'password': password} with the
        authentication parameters, or None if no authentication is used.
    """
    # Set up a dict containing authentication parameters for the MQTT client.
    if mqtt_config.username:
        # The password can be None.
        return {'username': mqtt_config.username,
                'password': mqtt_config.password}
    # Or use no authentication.
    else:
        return None


def host_port(mqtt_config):
    """Return the host and port from a :class:`.MQTTConfig` object.

    Args:
        mqtt_config (:class:`.MQTTConfig`): The MQTT connection settings.

    Returns:
        (str, int): A tuple with the host and port defined in the MQTT
        connection settings.
    """
    host_port = mqtt_config.broker_address.split(':')

    if mqtt_config.tls_hostname:
        host = mqtt_config.tls_hostname
    else:
        host = host_port[0]

    port = int(host_port[1])

    return (host, port)


def tls_params(mqtt_config):
    """Return the TLS configuration parameters from a :class:`.MQTTConfig`
    object.

    Args:
        mqtt_config (:class:`.MQTTConfig`): The MQTT connection settings.

    Returns:
        dict: A dict {'ca_certs': ca_certs, 'certfile': certfile,
        'keyfile': keyfile} with the TLS configuration parameters, or None if
        no TLS connection is used.
    """
    # Set up a dict containing TLS configuration parameters for the MQTT
    # client.
    if mqtt_config.tls_hostname:
        return {'ca_certs': mqtt_config.tls_ca_file,
                'certfile': mqtt_config.tls_client_cert,
                'keyfile': mqtt_config.tls_client_key}
    # Or don't use TLS.
    else:
        return None


def connect(client, mqtt_config, keepalive=60, bind_address=''):
    """Connect to an MQTT broker with the MQTT connection settings defined in
    an :class:`.MQTTConfig` object.

    Args:
        client (`paho.mqtt.client.Client`_): The MQTT client object.
        mqtt_config (:class:`.MQTTConfig`): The MQTT connection settings.
        keepalive (int, optional): The maximum period in seconds allowed
            between communications with the broker. Defaults to 60.
        bind_address (str, optional): The IP address of a local network
            interface to bind this client to, assuming multiple interfaces
            exist. Defaults to ''.

    .. _`paho.mqtt.client.Client`: https://www.eclipse.org/paho/clients/python/docs/#client
    """
    host, port = host_port(mqtt_config)

    # Set up MQTT authentication.
    auth = auth_params(mqtt_config)
    if auth:
        client.username_pw_set(auth['username'], auth['password'])

    # Set up an MQTT TLS connection.
    tls = tls_params(mqtt_config)
    if tls:
        client.tls_set(ca_certs=tls['ca_certs'],
                       certfile=tls['certfile'],
                       keyfile=tls['keyfile'])

    client.connect(host, port, keepalive, bind_address)


def publish_single(mqtt_config, topic, payload=None, qos=0, retain=False, client_id='', keepalive=60, will=None, protocol=MQTTv311, transport='tcp'):
    """Publish a single message to the MQTT broker with the connection settings
    defined in an :class:`.MQTTConfig` object, and then disconnect cleanly.

    Args:
        mqtt_config (:class:`.MQTTConfig`): The MQTT connection settings.
        topic (str): The topic string to which the payload will be published.
        payload (str, optional): The payload to be published. If '' or None, a
            zero length payload will be published.
        qos (int, optional): The qos to use when publishing. Defaults to 0.
        retain (bool, optional): Set the message to be retained (True) or not
            (False, default).
        client_id (str, optional): The MQTT client id to use. If '' or None,
            the Paho MQTT library will generate a client id automatically.
        keepalive (int, optional): The keepalive timeout value for the client.
            Defaults to 60 seconds.
        will (dict, optional): A dict containing will parameters for the
            client. Defaults to None, which indicates no will should be used.
        protocol (int, optional): The version of the MQTT protocol to use.
            Use either MQTTv31 or MQTTv311. Defaults to MQTTv311.
        transport (str): Set to 'websockets' to send MQTT over WebSockets.
            Leave at the default of 'tcp' to use raw TCP.
    """
    host, port = host_port(mqtt_config)
    auth = auth_params(mqtt_config)
    tls = tls_params(mqtt_config)

    single(topic, payload, qos, retain, host, port, client_id, keepalive, will, auth, tls, protocol, transport)
