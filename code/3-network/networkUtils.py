"""
    --------------------------------------------------------------------------------------
    networkUtils.py
    --------------------------------------------------------------------------------------
    Here are a few useful shortcut functions for working with networks.
    
    Some examples of use:
        import networkUtils
        networkUtils.connectToNetwork("mynetwork", "password")

        # Enable AP mode
        import networkUtils
        networkUtils.configureAP("atomant", "up up and away!")
        ap = networkUtils.getAccesspoint()
        print(ap.ifconfig())

        # Connect to a wifi network in Station mode
        import networkUtils
        networkUtils.connectToNetwork("network name", "password")
        station = networkUtils.getStation()
        print(station.ifconfig())
        print(station.isconnected())

    Author:  David Alexis (2019)
    -------------------------------------------------------------------------------------- 
"""

def getAccesspoint():
    import network

    return network.WLAN(network.AP_IF)


def getStation():
    import network

    return network.WLAN(network.STA_IF)


def configureAP(newEssid, newPassword):
    ap = getAccesspoint()
    currentEssid = ap.config('essid')

    if currentEssid != newEssid:
        ap.config(essid = newEssid, password = newPassword)
    else:
        ap.config(password = newPassword)

    print("Configured accesspoint %s" % (ap.config('essid')))


def connectToNetwork(networkName, password, disableAP=True):
    import time
    
    if disableAP == True:
        ap = getAccesspoint()
        
        if ap.active():
            ap.active(False)

    station = getStation()

    # Determine if station mode is active.  If it is not, enable it and
    # connect to the network
    if not station.active():
        station.active(True)

    if not station.isconnected() or station.config('essid') != networkName:
        station.connect(networkName, password)

        while station.isconnected():
            print('Waiting for network connection...')
            time.sleep(0.5)