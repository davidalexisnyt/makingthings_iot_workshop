"""
    --------------------------------------------------------------------------------------
    dhtSensorMqtt.py
    --------------------------------------------------------------------------------------
    Demonstrates how to connect to a remote MQTT message broker, and send temperature
    and humidity readings to a queue.

    Author:  David Alexis (2019)
    -------------------------------------------------------------------------------------- 
"""

import machine
import dht
import time
from umqtt.robust import MQTTClient
import gc


sensor = dht.DHT11(machine.Pin(16))
clientId = nc.mqtt_client
topic = b'temperature/humidity'
mqttFeedName = b'sensors/environment/office'
publishPeriodInSeconds = 10


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


# ------- Main program execution starts here --------

mqttClient = connect()

while True:
    print("reading...")
    
    try:
        # Get sensor readings
        sensor.measure()
        temperature = str(round((sensor.temperature() * (9 / 5)) + 32, 2))
        humidity = sensor.humidity()
        
        msg = b'{ "deviceId": "%s", "topic": "%s", "temp": { "value": %s, "unit": "F" }, "hum": { "value": %d, "unit": "percent" } }' % (clientId, topic, temperature, humidity)

        print(msg)
        
        mqttClient.publish(mqttFeedName, msg, qos=0)
        
        # Wait at least 2 seconds before next reading, since the DHT sensor can only
        # be read once every 2 seconds
        time.sleep(5)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqttClient.disconnect()
        sys.exit()
    except Exception as e:
        mqttClient = connect()