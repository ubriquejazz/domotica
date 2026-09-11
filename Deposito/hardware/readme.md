# Hardware

## CN3791, Maximum Power Point Tracking

With this MPPT charger for 6V solar panels, you can charge a lithium battery with a nominal voltage of 3.7V.

The maximum charge current can go up to 2A, depending on the capacity of the solar panel, and once the battery reaches 4.2V the battery charge is interrupted.

The output voltage is given directly by the battery.

Ref: [video in japanese](https://www.youtube.com/watch?v=pTtVe7P_lIc)

## 3V3 Buck Boost (TPS from Texas)

The CN3791 controller tracks the solar panel's sweet spot (MPPT) via buck conversion to safely charge a 1S Li-ion/LiPo battery (3.7V nominal, 4.2V max).

The TPS63060 regulator takes the variable battery voltage (2.8V to 4.2V) and seamlessly converts it to a stable output voltage of 3V3

## Max3485 Transceiver

| EN | Transceiver State | Current Draw | Behavior |
| -- | ----------------- | ------------ | -------- |
| **LOW** | **Receive Mode**  | **425 µA** | Driver is disabled. Receiver is active. The chip listens to the bus but transmits nothing. |
| **HIGH** | **Transmit Mode** | **15 mA to 30 mA** | Driver is active. Receiver is disabled. The chip transmits and ignores its own echo. |

## Ultrasonic

| Name | Comments |
|------|----------|
| AJ-SR04M () | R19 horizontal |
| SR04M-2 | R19 vertical |
| RCWL-1655 | R7 horizontal |

### RCWL-1655

Trig high for more than 10 us; Echo is proportional to the distance.

Baudrate = 9600 N 8 1. The PC send a command:
- 0xF1, after a while the module return its version
- 0xA0, after a while the module return the distance in mm

Write 0x01 to the I2C address 0x57, and wait for 100ms (maximum ranging time)	
- distance_mm = (High << 16) + (Medium << 8) + Low

|             | Min  | Typ  | Max  |      |
| ----------- | ---- | ---- | ---- | ---- |
| Voltage     | 2.8  |      | 5.5  | V    |
| Current     |      | 3.5  |      | mA   |
| Distance    | 20   |      | 500  | cm   |
| Angle       |      | +-20 |      | §    |
| Work        |      | 40   |      | KHz  |
| Sampling    |      | 50   |      | ms   |
| Temperature | -10  |      | 60   | §    |

References:
- [Modes](https://www.youtube.com/watch?v=n0hFgR4hYqY)
- [Datasheet](https://www.fabian.com.mt/viewer/42585/pdf.pdf)
- [Electroya](https://www.electroya.com/producto/aj-sr04m-nueva-version-modulo-ultrasonico-impermeable-3-55-v-con-sonda/)

