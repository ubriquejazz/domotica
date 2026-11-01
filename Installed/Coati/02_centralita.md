# 2. Central Control Unit

## 2.1 Initial Setup

The central unit uses a four-digit security code to access its functions. The factory default code is:

**1234**

To start the system:

1. Insert the batteries.
2. The Status LED should illuminate for approximately one second and then turn off, confirming that the unit has powered up correctly.
3. If no sensor IDs have been registered, the Status LED will flash every three seconds.

The alarm will stop this periodic flashing once at least one sensor ID has been learned.

## 2.2 Keypad Commands

All functions are accessed by entering the four-digit security code followed by the corresponding mode key.

| Keypad sequence | Function |
|---|---|
| `1234 + 1` | Instant alarm mode |
| `1234 + 2` | Delayed alarm mode |
| `1234 + 3` | Chime mode |
| `1234 + 4` | Disarm alarm / chime |
| `1234 + 6` | Change security code |
| `1234 + 8` | Enable keypad tones |
| `1234 + *` | Learn sensor IDs |
| `1234 + #` | Clear sensor IDs |

**Important:** The default security code should be changed during initial setup.

## 2.3 Registering Wireless Sensors

The central unit can store up to 12 sensor IDs. Each wireless sensor must be registered before it can activate the alarm.

To register a sensor:

1. Enter the security code followed by `*`.
2. The Status and Charge LEDs will start flashing, indicating that the unit is in learning mode.
3. Activate the sensor's ID transmission procedure (see the relevant sensor section).
4. When registration is successful, the central unit emits a long beep.
5. The unit automatically returns to disarmed mode.

The learning procedure has a **30-second timeout**. If no sensor ID is received within this period:

- The unit automatically exits learning mode.
- The Status LED flashes four times rapidly.

During learning mode, normal keypad inputs and sensor activations are ignored.

## 2.4 Clearing Registered Sensor IDs

To erase the registered sensor IDs:

1. Enter the security code followed by `#`.
2. Both the Status and Charge LEDs will illuminate continuously.

The original documentation does not specify a separate confirmation procedure after clearing the IDs.

## 2.5 Arming the Alarm

The system provides two alarm modes.

### Instant alarm mode

1. Enter the security code followed by `1`.
2. The central unit starts a 5-second exit countdown.
3. During the countdown:
   - The unit emits audible beeps.
   - The Status LED flashes.
4. After 5 seconds, the alarm becomes armed.

### Delayed alarm mode

1. Enter the security code followed by `2`.
2. The central unit starts a 15-second exit countdown.
3. During the countdown:
   - The unit emits audible beeps.
   - The Status LED flashes.
4. After 15 seconds, the alarm becomes armed.

## 2.6 Chime Mode

Chime mode allows the system to operate while occupants are inside the property.

When a registered sensor is activated, the central unit produces a chime instead of triggering the security alarm.

To activate chime mode:

1. Enter the security code followed by `3`.

This mode is recommended when the property is occupied, as it avoids repeated full alarm activations.

## 2.7 Disarming the System

To disarm the alarm:

1. Enter the security code followed by `4`.

Once disarmed:

- Alarm activation is disabled.
- Signals received from registered sensors are ignored.

## 2.8 Alarm Activation

When the alarm is triggered, the central unit operates according to the following cycle:

- Alarm sounds for 30 seconds.
- Alarm remains silent for 10 seconds.
- This cycle repeats up to 10 times.

## 2.9 Changing the Security Code

The security code can be changed using the following keypad command:

`Current security code + 6`

The original documentation does not provide the subsequent steps for entering and confirming the new code.

## 2.10 Keypad and LED Indications

When a valid security code and mode key are entered:
- The central unit emits a long beep.
- The Status LED illuminates.

When an incorrect security code is entered:
- The Charge LED flashes.
- The unit emits three beeps.

After three consecutive incorrect attempts, the keypad is disabled for 30 seconds.

If keypad entry is not completed within 10 seconds, the current input is cancelled.

# 2.11 LED Indications

| LED behaviour | Meaning |
|---|---|
| Illuminated continuously | The device is transmitting a radio signal. |
| Flashes every 30 seconds | Low battery. |

These indications are sensor-related. The original documentation does not specify whether they apply identically to both sensor models