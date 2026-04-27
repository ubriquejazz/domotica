# Aguas abajo

![](fig/sensor.png)

Alternativas al Arduino Nano

- La raspberry recibe el mensaje UART y lo muestra en un gauge (node-red)
- Este [esphome](https://esphome.io/components/sensor/jsn_sr04t/) lo expone en home-assistant
- Hacer un **daisy chain** arduino + esp32 para poder mostrar el nivel un LCD

## Alimentacion

- Por grid de la casa
- Por paneles + baterias de 12V

## Red Wifi

- Flybox + SIM 4G (3 euros)
- Home assistant (RPi4)
- Kiosk (PiZero) detras de la puerta
- DIY or BUY aleman: [video](https://www.youtube.com/watch?v=jriRW4rGQp4&t=224s)

### Material

- RP2040 Raspbery Pico, USB-C + LCD
- Step-down 12V/24V a 5V (USB)

- Módulo RS485 TTL para 100m

![](fig/max485.png)
