# Automatic Boiler
## Introduction
This project is created to turn on/off devices remotely. This turn on/off system is MQTT distribuited. Although server and UI is running in the same RPi, the system is flexible enough to run everything in different platforms. These are the system roles:

- MQTT broker where the entire MQTT protocol runs
- MQTT **main** client where timing is controlled and options are saved in a config file (boiler.py)
- MQTT hardware clients: to set power on/off some device (boiler.ino)
- Web server where the UI is developed, with a MQTT client to send/receive values (functions.js)

And these are the real hardware devices of the system:
- **Raspberry Pi** where MQTT server, main client and web server runs
- **ESP device** connected to a relay that turn on/off appliances, where an MQTT client is running

## RPi Clients

### MQTT javascript client (html/functions.js)
Initially this client publishes a message with the topic 'home/params/get'

Once it's connected to the broker, it's subscribed to these topics to update the web page:
1. home/relay/status
2. home/params/status/#

There are some drop-down lists with times and temperatures to be writen in the config file. This is done by publishing messages with the topic 'home/params/set/#'

### MQTT main client (rpi/boiler.py)
This client is subscribed to two topics:
1. home/params/set/# 
2. home/params/get

The first one is to update the config file from the javascript, the other one is to read the config file and publish it within the topics home/params/status/#. 

Finally, the client is subscribed to home/relay/status but it's ignored because it is managed directly by the HW device and received by the javascript client.

There is a controller object to generate a signal to turn on the relay (home/relay/set 1) depending on the current time and temperature. 

## Tests

### Scenario 1

Button on the web browser to read the config file (connect).

|Javascript             | Boiler.py |
|-----------------------|-------------------------------------|
| function onConnect()  ||
| send home/params/get | def on_message() |
|                       | read config file |
|                       | send home/params/status/# |
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
| send home/params/set/# | def on_message() |
|                       | if home/params/set/user_temp
|                       | update config file
|                       | send home/params/status/user_temp
| function onMessageArrived() ||
| update html           ||