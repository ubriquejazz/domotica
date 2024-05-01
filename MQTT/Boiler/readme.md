# Automatic Boiler
## Introduction
This project is created to turn on/off devices remotely. This turn on/off system is MQTT distribuited. Although server and UI is running in the same RPi, the system is flexible enough to run everything in different platforms. These are the system roles:

- MQTT broker where the entire MQTT protocol runs
- MQTT **main** client where timing is controlled and options are saved to be sent when needed
- MQTT hardware clients: to set power on/off some device
- Web server where the UI is developed, with a MQTT client to send/receive values (javascript)

And this is the real hardware devices of the system
- **Raspberry Pi** where MQTT server, main client and web server runs
- **ESP01** connected to a relay that turn on/off hardware devices, where an MQTT client is running

## ESP01
- In Arduino IDE, go to Preferences->URL manager
- Fill the field with `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
- Install the library in the manager and choose "Generic ESP8266 module"
- Go to the library manager and install PubSubClient library
- Install de driver of the programmer (with the device already connected): http://sparks.gogo.co.nz/assets/_site_/downloads/CH340_WINDOWS.zip

## Raspberry Pi
### Web server
In order to have a web page as a UI available, an Apache server is needed:
```
sudo apt install apache2 -y
```
Try to connect to http://localhost/ from the RPi or http://xxx.xxx.x.xxx/ whatever the ip of the raspbery is. The webpage of apache server is in `/var/www/html/`. Everytime you need to apply changes in your server you must cp the `html` folder from the git repository to there:
```
cd automatic_boiler
cp -r html /var/www/
```
### MQTT broker 
To run this project Mosquitto broker is used. To download it type:
```
sudo apt-get -y install mosquitto mosquitto-clients
```
Enable Mosquitto service in your system control:
```
sudo systemctl enable mosquitto.service
```
As a daemon, Mosquitto will start everytime system is turned on. For the first test, you have to enable to start working:
```
mosquitto -d
```
You need to know the IP address of the server to connect clients.

### MQTT javascript client
Paho is web browser based and uses WebSockets to connect to brokers. In order to get the Paho library of python: `pip3 install paho-mqtt`

This client library is popular because programmers don’t need to deal with the possibility of port 1833 being blocked.

```
cd /etc/mosquitto/conf.d
sudo nano local.conf
listener 1883
protocol mqtt
listener 8080
protocol websockets
```

### MQTT main client
```
crontab -e
@reboot sleep 30; cd /path_to_code/automatic_boiler/src/rpi; /usr/bin/python3 boiler.py
```