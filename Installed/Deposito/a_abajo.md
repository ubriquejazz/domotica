# Aguas abajo

Opcion 1 - simplest
- La raspberry recibe el mensaje UART y lo muestra en un gauge (node-red)

Opcion 2 - home-assistant
- Este [esphome](https://esphome.io/components/sensor/jsn_sr04t/) es para el ultrasonido SR04M-2

Opcion 3 - con LCD local 
- Hacer un **daisy chain** Pico + ESP32 para poder mostrar el nivel en un LCD

## Infraestructura (casa)

- Flybox + SIM 4G (3 euros)
- Home assistant (RPi4)
- Kiosk (PiZero) detras de la puerta
- DIY or BUY aleman: [video](https://www.youtube.com/watch?v=jriRW4rGQp4&t=224s)

### Material

- RP2040 Raspbery Pico, USB-C + LCD
- Step-down 12V/24V a 5V (USB)
- Módulo RS485 TTL para 100m

| Nombre | Vista |
|--------|-----------|
| RS485   |  ![](fig/max485.png)
