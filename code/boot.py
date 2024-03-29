"""
    --------------------------------------------------------------------------------------
    boot.py
    --------------------------------------------------------------------------------------
    This file (boot.py) is executed on every boot (including wake-boot from deepsleep).
    The MicroPython runtime first looks for a file called boot.py, and executes if it exists.
    It then looks for a file called main.py, which should contain the entry point for the
    main functionality of your project.

    Author:  David Alexis (2019)
    --------------------------------------------------------------------------------------
"""

import esp
import uos
import machine
# uos.dupterm(None, 1) # disable REPL on UART(0)
import gc

esp.osdebug(None)
gc.collect()


def do_connect(networkName, password):
    """
        This function connects to your network of choice in station (client) mode
        if it is not already connected.
        The ESP8266 generally remembers the last network to which it had successfully
        connected, and will automatically connect again.
    """

    import network

    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(networkName, password)

        while not sta_if.isconnected():
            pass

    print('network config:', sta_if.ifconfig())


def startWebRepl():
    """
        MicroPython comes with the ability to expose the Python REPL as a website
        from the device.  This works whether the device is in access point or
        station mode.  You just need to know the IP address of the device.
        Connecting to http://<device IP>:8266 in a browser will display the REPL
        interface.
        This function enables the web REPL.
    """
    import webrepl
    webrepl.start()
