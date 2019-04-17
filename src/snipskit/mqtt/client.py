"""This module contains helper functions to use the MQTT protocol with the MQTT
broker defined in a :class:`.MQTTConfig` object.
"""


def connect(client, mqtt_config, keepalive=60, bind_address=''):
    """Connect to an MQTT broker with the MQTT connection settings defined in
    an :class:`.MQTTConfig` object.

    Args:
        client (`paho.mqtt.client.Client`_): The MQTT client object.
        mqtt_config (:class:`.MQTTConfig`): The MQTT connection settings.
        keepalive (int, optional): The maximum period in seconds allowed
            between communications with the broker. Default value: 60.
        bind_address (str, optional): The IP address of a local network
            interface to bind this client to, assuming multiple interfaces
            exist. Default value: empty string.

    .. _`paho.mqtt.client.Client`: https://www.eclipse.org/paho/clients/python/docs/#client
    """
    host_port = mqtt_config.broker_address.split(':')

    # Set up MQTT authentication.
    if mqtt_config.username:
        # The password can be None.
        client.username_pw_set(mqtt_config.username, mqtt_config.password)

    # Set up an MQTT TLS connection.
    if mqtt_config.tls_hostname:
        client.tls_set(ca_certs=mqtt_config.tls_ca_file,
                       certfile=mqtt_config.tls_client_cert,
                       keyfile=mqtt_config.tls_client_key)
        host = mqtt_config.tls_hostname
    # Or set up an insecure connection.
    else:
        host = host_port[0]

    port = host_port[1]

    client.connect(host, int(port), keepalive, bind_address)
