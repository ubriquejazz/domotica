# Raspberry Setup

## Web server
In order to have a web page as a UI available, an Apache server is needed:
```
sudo apt install apache2 -y
```
Try to connect to http://localhost/ from the RPi or http://xxx.xxx.x.xxx/ whatever the ip of the raspbery is. The webpage of apache server is in `/var/www/html/`. Everytime you need to apply changes in your server you must cp the `html` folder from the git repository to there:
```
cd automatic_boiler
cp -r html /var/www/
```
## MQTT broker 
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

### MQTT main client (boiler.py)
```
crontab -e
@reboot sleep 30; cd /path_to_code/automatic_boiler/src/rpi; /usr/bin/python3 boiler.py
```