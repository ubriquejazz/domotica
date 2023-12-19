import socket
import machine
import network

# WLAN credentials
wifissid = 'yourwifissid'
wifipass = 'yourwifipass'

# Global
wifi = network.WLAN(network.STA_IF)
    
# HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head>
<title>Car</title>
<style>
body {background-color: black}
h1 {color:red}
button {
        color: white;
        height: 200px;
        width: 200px;
        background:black;
        border: 3px solid #4CAF50; /* Green */
        border-radius: 50%;
        font-size: 250%;
        position: center;
}
</style>
</head>
<body>
<center>
<form>
<div><button name="CMD" value="l" type="submit">L</button>
<button name="CMD" value="forward" type="submit">Forward</button>
<button name="CMD" value="r" type="submit">R</button></div>
<div><button name="CMD" value="left" type="submit">Ls</button>
<button name="CMD" value="stop" type="submit">Stop</button>
<button name="CMD" value="right" type="submit">Rs</button></div>
<div><button name="CMD" value="back" type="submit">Back</button></div>
<div><button name="CMD" value="slow" type="submit">Slow</button>
<button name="CMD" value="mid" type="submit">Mid</button>
<button name="CMD" value="fast" type="submit">Fast</button>
<button name="CMD" value="auto" type="submit">Auto</button></div>
</form>
</center>
</body>
</html>
"""

# connect the device to the WiFi network
def newConnection():
    wifi.active(True)
    wifi.connect(wifissid,wifipass)
    count = 7
    while not wifi.isconnected() and count > 0 :
        count -= 1
        print ('.')
        time.sleep(1)

    if wifi.isconnected() :
        print('network config:', wifi.ifconfig())
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 80))
        s.listen(5)
        print("Listening, connect your browser to http://<this_host>:80/")
    else  :
        print('No Wifi. Auto Mode')
        auto = True
        
def remoteControl () :
    global auto, s, action, speed
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)

    if request.find('/?CMD=forward') == 6:
        print('+forward')
        action = 1
    elif request.find('/?CMD=back') == 6:
        print('+back')
        action = 2
    elif request.find('/?CMD=left') == 6:
        print('+left')
        action = 3
    elif request.find('/?CMD=right') == 6:
        print('+right')
        action = 4
    elif request.find('/?CMD=l') == 6:
        print('+L')
        action = 5
    elif request.find('/?CMD=r') == 6:
        print('+R')
        action = 6
    elif request.find('/?CMD=stop') == 6:
        print('+stop')
        action = 0
    elif request.find('/?CMD=fast') == 6:
        print('+fast=')
        speed = maxSpeed
        print (speed)
    elif request.find('/?CMD=slow') == 6:
        print('+slow=')
        speed = minSpeed
        print (speed)
    elif request.find('/?CMD=mid') == 6:
        print('+mid=')
        speed = midSpeed
        print (speed)
    elif request.find('/?CMD=man') == 6:
        auto=False
        action = 0
        print('+manual=')
    elif request.find('/?CMD=auto') == 6:
        auto=True
        action = 0
        print('+autoDrive')

    if action == 0:
        stop ()
    elif action == 1:
        forward()
    elif action == 2:
        back()
    elif action == 3:
        left()
    elif action == 4:
        right()
    elif action == 5:
        left_cruise()
    elif action == 6:
        right_cruise()

    response = html
    conn.send(response)
    conn.close()
    