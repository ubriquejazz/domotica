# ESP32_Micropython_Robotic_Car

Authors: cheungbx  2020/04/30, ubriquejazz 2021/12/22

Pin layout from each module to the AZDelivery ESP32 D1 R32 WLAN

**L298N motor module**

|      | Arduino | ESP32   |
| ---- | ------- | ------- |
| IN1  | D7      | GPIO-14 |
| IN2  | D8      | GPIO-12 |
| IN3  | D9      | GPIO-13 |
| IN4  | D11     | GPIO-23 |
| ENA  | D6      | GPIO-27 |
| ENB  | D5      | GPIO-16 |

**Ultrasound HCSR04**

|      | Arduino | ESP32   |
| ---- | ------- | ------- |
| Echo | A4      | GPIO-36 |
| Trig | A5      | GPIO-39 |
| PWM  | D3      | GPIO-25 |

**Line Tracking** 

|       | Arduino | ESP32   |
| ----- | ------- | ------- |
| Right | D10     | GPIO-5  |
| Med   | D4      | GPIO-17 |
| Left  | D2      | GPIO-26 |

**Infrared Sensor**

|       | Arduino | ESP32   |
| ----- | ------- | ------- |
| Input | D12     | GPIO-19 |



**Note**: Unboxing Elegoo Smart Car Arduino Robot KIT Version 3.0
https://www.youtube.com/watch?v=puHBcII1Qt8&list=PLkFeYZKRTZ8ZoGLVI1El1_pJ0S1G0nnKK

