# Raspberry Setup

## Web server
In order to have a web page as a UI available, an Apache server is needed:
```
sudo apt install lighttpd
```
The webpage of  server is in `/var/www/html/`. Everytime you need to apply changes in your server you must cp the `html` folder from the git repository to there:
```
cd domotica/Boiler
cp -r html /var/www/
```
It also works with the script`install_boiler_web.sh` (better becase of the right credentials).

## MQTT broker 

To run this project Mosquitto broker is used. To enable Mosquitto service in your system control:
```
sudo systemctl enable mosquitto.service
```
As a daemon, Mosquitto will start everytime system is turned on. For the first test, you have to enable to start working:
```
mosquitto -d
```
You need to know the IP address of the server to connect clients.

### MQTT javascript client (html/functions.js)

Paho is web browser based and uses WebSockets to connect to brokers (you don’t need to deal with the possibility of port 1833 being blocked):

```
cd /etc/mosquitto/conf.d
sudo nano local.conf
listener 1883
protocol mqtt
listener 8080
protocol websockets
```