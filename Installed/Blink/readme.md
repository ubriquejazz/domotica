# RM Pro (RM3)

Make sure your phone is connected to the 2GHz network in the area where the RM Pro is. 

- Open the BroadLink IR app, input Wi-Fi password and press Configure.
- Use the auto connect method

After you've connected, you'll find the Wi-Fi light on the RM Pro is off and there is a new RM Pro in the device list of the app:

- AC Midea (Eluxe Leroy Merlin)
- Robot iLife [V7s Plus](https://www.youtube.com/watch?v=k0CUnGYODLM)

## How to use it with [MQTT](https://github.com/eschava/broadlink-mqtt) commands

**Recording (IR or RF)**

To record new command just send *record* message for IR command or *recordrf* for RF command to the **topic broadlink/COMMAND_ID**, where COMMAND_ID is any identifier that can be used for file name (slashes are also allowed)

Example: to record power button for Samsung TV send

    record -> broadlink/tv/samsung/power

and recorded interpretation of IR signal will be saved to file commands/tv/samsung/power

**Replay**

To replay previously recorded command send replay message to the topic broadlink/COMMAND_ID,
where COMMAND_ID is identifier if the command

Example: to replay power button for Samsung TV send

```
replay -> broadlink/tv/samsung/power
```

and saved interpretation of IR signal will be replayed from file commands/tv/samsung/power

Another format for replaying recorded command is using file name as a message and folder as MQTT topic. Example: to replay power button for Samsung TV send

```
power -> broadlink/tv/samsung
```

and saved interpretation of IR signal will be replayed from file commands/tv/samsung/power