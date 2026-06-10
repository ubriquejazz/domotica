
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