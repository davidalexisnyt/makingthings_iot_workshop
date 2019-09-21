"""
    --------------------------------------------------------------------------------------
    mqttSubscriber.py
    --------------------------------------------------------------------------------------
    Demonstrates how to subscribe to an MQTT topic.  This script can be used on an IoT
    device, or on a desktop/laptop.

    Author:  David Alexis (2019)
    -------------------------------------------------------------------------------------- 
"""

import network
import machine
import time
import os
import gc
import sys
import ubinascii
from umqtt.robust import MQTTClient

# WiFi connection information
WIFI_SSID = 'makingthings-iot'
WIFI_PASSWORD = 'rusty-rabbit'
mqtt_server = '10.3.141.1'
mqtt_feedname = b'sensors/environment/office'


def subscription_handler(topic, msg):
    print(topic, " :: ", msg)


def connect():
    import networkCredentials as nc
    import networkUtils    

    print("Connecting...")
    
    networkUtils.connectToNetwork(nc.wifi_network, nc.wifi_password)

    print("Connecting to Mqtt...")
    
    client = MQTTClient(client_id=nc.mqtt_client,
                    server=nc.mqtt_server,
                    user=nc.mqtt_user,
                    password=nc.mqtt_password,
                    ssl=False)
    client.connect()
    
    print("Connected")
    
    return client


# ------ Main script execution starts here ------

gc.collect()

client_id = b"receiver_{}".format(ubinascii.hexlify(machine.unique_id()))
topic = b'temperature'

client = connect()

while True:
    try:
        client.check_msg()
        time.sleep(1)
    except Exception as e:
        client = connect()