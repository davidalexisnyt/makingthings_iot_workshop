"""
    --------------------------------------------------------------------------------------
    dhtSensor.py
    --------------------------------------------------------------------------------------
    This script shows hot to use the DHT 11 digital humidity and temperature sensor.
    These sensors cost around $3 or $4.
    The sensor provides temperature values in Celcius, which can then be easity converted
    to Fahrenheit if needed.  The sensors can only read measurements every 2 seconds, so
    a delay needs to be inserted between readings.

    Author:  David Alexis (2019)
    -------------------------------------------------------------------------------------- 
"""

import machine
import dht
import time

import gc
gc.collect()

sensor = dht.DHT11(machine.Pin(16))

while True:
    # Get sensor readings
    sensor.measure()
    temperature = sensor.temperature()
    temperatureF = str(round(temperature * 1.8 + 32, 2))
    humidity = sensor.humidity()
    
    reading = {
        "temperature": temperatureF,
        "humidity": humidity
    }
    
    print(reading)
    
    # Wait at least 2 seconds before next reading, since the DHT sensor can only
    # be read once every 2 seconds
    time.sleep(5)