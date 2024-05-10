# Automatic Boiler
## Introduction
This project is created to turn on/off devices remotely. This turn on/off system is MQTT distribuited. Although server and UI is running in the same RPi, the system is flexible enough to run everything in different platforms. These are the system roles:

- MQTT broker where the entire MQTT protocol runs
- MQTT **main** client where timing is controlled and options are saved in a config file (json)
- MQTT hardware clients: to set power on/off some device
- Web server where the UI is developed, with a MQTT client to send/receive values (javascript)

And this is the real hardware devices of the system
- **Raspberry Pi** where MQTT server, main client and web server runs
- **uC** connected to a relay that turn on/off hardware devices, where an MQTT client is running

## RPi Clients

### MQTT javascript client (html/functions.js)
Initially this client publishes two **get** messages: 
1. /home/relay/get 
2. /home/params/get

Once it's connected to the broker, it's subscribed to some topics to update the web page:
1. /home/relay/status
2. /home/params/stauts

There are some drop-down lists with times and temperatures to be writen in the config file. This is done by publishing messages in the topic home/params/set/#

### MQTT main client (src/rpi/boiler.py)

This client is subscribed to two topics:
1. /home/params/set/# 
2. /home/params/get

The first one is to update the config file from the javascript, the other one is to read the config file and publish it within the topics home/params/status/#. 

Finally, the client is subscribed to /home/relay/status but it's ignored because it is served by the javascript client.

There is a controller object to generate a signal to turn on the relay (home/relay/set 1) depending on the current time and temperature. 

## Tests

### Scenario 1

Button on the web browser to read the config file (connect).

|Javascript             | Boiler.py |
|-----------------------|-------------------------------------|
| function onConnect()  ||
| send /home/params/get | def on_message() |
|                       | read config file |
|                       | send /home/params/status/# |
| function onMessageArrived() ||
| update html           ||

### Scenario 2

Command to turn the relay on (user temperature simulation).

```
mosquitto_pub -t 'home/relay/set' -m 1
```

### Scenario 3

Update the config file from the web browser (user temperature).

|Javascript             | Boiler.py |
|-----------------------|-------------------------------------|
| function setUserTemp()  ||
| send /home/params/set/# | def on_message() |
|                       | if home/params/set/user_temp
|                       | update config file
|                       | send home/params/status/user_temp
| function onMessageArrived() ||
| update html           ||