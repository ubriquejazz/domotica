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

References:
- [Modes](https://www.youtube.com/watch?v=n0hFgR4hYqY)
- [Datasheet](https://www.fabian.com.mt/viewer/42585/pdf.pdf)