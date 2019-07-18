from machine import Pin
from machine import ADC
import time

tmp36 = ADC(0)


def readCelcius(sensor):
    return sensor.read() / 10


def readFahrenheit(sensor):
    celsius = readCelcius(sensor)
    return (celsius * (9 / 5)) + 32


while True:
    temperature = readCelcius(tmp36)
    print(temperature)

    time.sleep(1)
