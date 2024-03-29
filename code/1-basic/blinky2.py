"""
    --------------------------------------------------------------------------------------
    blinky2.py
    --------------------------------------------------------------------------------------
    Shows a slightly different way to access the Pin class, refactors the toggling of the
    LED into a reusable function, and performs 

    Author:  David Alexis (2019)
    -------------------------------------------------------------------------------------- 
"""

# Here we import the Pin class from the machine module so that we don't have to refer
# to it with "machine.Pin".
from machine import Pin
import time

def blink(led_pin, duration):
    """
    Turn on the LED for the specified amount of time, then turn it off
    """
    led_pin.on()
    time.sleep_ms(duration)
    led_pin.off()


# ------- Main program execution starts here --------

led = Pin(2, Pin.OUT)

while True:
    blink(led, 500)
    blink(led, 500)
    blink(led, 2000)