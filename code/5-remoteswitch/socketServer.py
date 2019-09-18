"""
    --------------------------------------------------------------------------------------
    socketServer.py
    --------------------------------------------------------------------------------------
    Serves a web page from the ESP8266 that allows remotely turning a light on and off

    Author:  David Alexis (2019)
    -------------------------------------------------------------------------------------- 
"""

import socket
import machine
import os
import gc
import networkCredentials as nc
import networkUtils
from machine import Pin

led = Pin(2, Pin.OUT)

def htmlPage():
    if led.value() == 1:
        is_led_on = "ON"
    else:
        is_led_on = "OFF"
    
    html = """
        <html>
            <head>
                <title>Remote Light Switch</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="icon" href="data:,">
                <style>
                    html {
                        font-family: Helvetica;
                        display: inline-block;
                        margin: 0px auto;
                        text-align: center;
                    }

                    h1 {
                        color: #0F3376;
                        padding: 2vh;
                    }

                    p {
                        font-size: 1.5rem;
                    }

                    .button {
                        display: inline-block;
                        background-color: #e7bd3b;
                        border: none;
                        border-radius: 4px;
                        color: white;
                        padding: 16px 40px;
                        text-decoration: none;
                        font-size: 30px;
                        margin: 2px;
                        cursor: pointer;
                    }

                    .button2 {
                        background-color: #4286f4;
                    }
                </style>
            </head>

            <body>
                <h1>Remote Light Switch</h1>
                <p>Light is currently <strong>""" + is_led_on + """</strong></p>
                <p><a href="/?led=on"><button class="button">ON</button></a></p>
                <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
            </body>
        </html>
    """
    return html


# Start the garbage collector
gc.collect()


# ------ Main script execution starts here ------

networkUtils.connectToNetwork(nc.wifi_network, nc.wifi_password)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 80))
sock.listen(5)

while True:
    try:
        print("Waiting")
        connection, address = sock.accept()
        print("Got connection from {}".format(address))

        request = str(connection.recv(1024))
        
        if request.find('/?led=on') == 6:
            print('LED ON')
            led.on()
        if request.find('/?led=off') == 6:
            print('LED OFF')
            led.off()

        response = htmlPage()
        
        connection.send('HTTP/1.1 200 OK\n')
        connection.send('Content-Type: text/html\n')
        connection.send('Connection: close\n\n')
        connection.sendall(response)
        connection.close()
    except:
        pass