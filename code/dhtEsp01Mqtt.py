import machine
import network
import dht
import time
from umqtt.robust import MQTTClient
import gc
import esp
import networkCredentials as nc

esp.osdebug(None)
gc.collect()

sensor = dht.DHT11(machine.Pin(16))

clientId = b"09-E5-12-03"
topic = b'temperature/humidity'
mqttServer = 'makingthingsiot2'  #'10.3.141.1'
mqttFeedName = b'sensors/environment/' + clientId
publishPeriodInSeconds = 10


def connect():
    print("Connecting to " + nc.wifi_network)
    
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    
    station = network.WLAN(network.STA_IF)
    
    if not station.active():
        station.active()
    
    #station.connect("makingthings-iot", "rusty-rabbit")
    station.connect(nc.wifi_network, nc.wifi_password)
    
    while not station.isconnected():
        print("waiting...")
        time.sleep(1)

    try:
        from ntptime import settime
        setttime()
    except:
        pass
    
    print(str(time.localtime()))
    
    client = MQTTClient(client_id=clientId,
                    server=mqttServer,
                    user='makingthingsiot',
                    password='sirmakesalot',
                    ssl=False)
    client.connect()
    
    print("Connected")
    
    return client

# ------- Main program execution starts here --------

mqttClient = connect()
start = 0
delta = 0

while True:
    if start == 0:
        start = time.ticks_ms()
    else:
        delta = time.ticks_diff(time.ticks_ms(), start)
    
    if delta >= 5000:
        print("reading...")
        
        start = time.ticks_ms()
        
        try:
            mqttClient.check_msg()
            
            try:
                # Get sensor readings
                sensor.measure()
                temperature = (sensor.temperature() * (9 / 5)) + 32
                humidity = sensor.humidity()
                
                now = time.localtime()
                timestamp = "{:d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(now[0], now[1], now[2], now[3], now[4], now[5])
                msg = b'{ "deviceId": "%s", "timestamp": "%s", "topic": "%s", "temp": { "value": %f, "unit": "F" }, "hum": { "value": %d, "unit": "percent" } }' % (clientId, timestamp, topic, temperature, humidity)
            except Exception as e:
                msg = b'{ "deviceId": "%s", "topic": "%s", "error": "%s" }' % (clientId, topic, e)
                print(e)
                
            print(msg)
            
            mqttClient.publish(mqttFeedName, msg, qos=0)
            
            # Wait at least 2 seconds before next reading, since the DHT sensor can only
            # be read once every 2 seconds
            
        except KeyboardInterrupt:
            #print('Ctrl-C pressed...exiting')
            mqttClient.disconnect()
            sys.exit()
        except Exception as e:
            print(e)
            mqttClient = connect()
            
    time.sleep(.5)