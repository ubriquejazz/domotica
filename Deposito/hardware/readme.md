

## Maximum Power Point Tracking

The MPPT 

With this MPPT CN3791 solar manager for 6V solar panels, you can charge a lithium battery with a nominal voltage of 3.7V.

The maximum charge current can go up to 2A, depending on the capacity of the solar panel, and once the battery reaches 4.2V the battery charge is interrupted.

The output voltage is given directly by the battery.

## 3V3 Buck Boost (TPS from Texas)

The CN3791 controller tracks the solar panel's sweet spot (MPPT) via buck conversion to safely charge a 1S Li-ion/LiPo battery (3.7V nominal, 4.2V max).

The Output Regulation Stage (TPS63060): Takes the variable battery voltage (2.8V to 4.2V) and seamlessly converts it to a stable output voltage of 3V3


## 485 Transceivers


| EN | Transceiver State | Current Draw | Behavior                                                     |
| ------------------- | ----------------- | -------------------- | ------------------------------------------------------------ |
| **LOW (0V)**        | **Receive Mode**  | **425 µA**           | Driver is disabled. Receiver is active. The chip listens to the bus but transmits nothing. |
| **HIGH (3.3V)**     | **Transmit Mode** | **15 mA to 30 mA**   | Driver is active. Receiver is disabled. The chip transmits your data and ignores its own echo. |