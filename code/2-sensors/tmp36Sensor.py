"""
    --------------------------------------------------------------------------------------
    tmp36Sensor.py
    --------------------------------------------------------------------------------------
    Demonstrates how to use the TMP36 analog temperature sensor.  These sensors are
    relatively cheap, very accurate, and easy to use.  It provides temperature readings as
    a relative voltage, which is then converted to a Celcius value.

    Author:  David Alexis (2019)
    -------------------------------------------------------------------------------------- 
"""

from machine import Pin
from machine import ADC
import time

# The sensor must be connected to the analog/digital converter pin on the ESP8266.
# The ESP8266 has only one analog pin, represented as A0 on the board.
tmp36 = ADC(0)


def readCelcius(sensor):
    return sensor.read() / 10


def readFahrenheit(sensor):
    celsius = readCelcius(sensor)
    return celsius * 1.8 + 32


while True:
    temperature = readFahrenheit(tmp36)
    print(temperature)

    time.sleep(2)
