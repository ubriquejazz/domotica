# Aguas abajo

Opcion 1 - simplest
- La raspberry recibe el mensaje UART y lo muestra en Javascript

Opcion 2 - home-assistant
- Este [esphome](https://esphome.io/components/sensor/jsn_sr04t/) es para el ultrasonido SR04M-2

Opcion 3 - LCD local 
- ESP32 para poder mostrar el nivel en un LCD

## Infraestructura (casa)

- Solar panel and 12V batteries

  - Step-down 12V/24V a 5V (USB)
  - Flybox + SIM 4G (3 euros)
  - ESP32 and LCD

- Home assistant (RPi4)

- Kiosk (PiZero) detras de la puerta

  

### Material

- RP2040 Raspbery Pico, USB-C + LCD
- Módulo RS485 TTL para 100m

| Nombre | Vista |
|--------|-----------|
| RS485   |  ![](fig/max485.png)



- DIY or BUY aleman: [video](https://www.youtube.com/watch?v=jriRW4rGQp4&t=224s)

- I2C LCD library for Pico: https://github.com/T-622/RPI-PICO-I2C-LCD

- I2C LCD library for ESP32, Pico, etc: https://github.com/DIYables/DIYables_MicroPython_LCD_I2C

  
