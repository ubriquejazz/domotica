# Deposito Water level

## Aguas abajo

La PiZero recibe un mensaje UART y lo muestra en un gauge (node-red)

- PiZero + Max485 + 100m cable
- MPTT para Router 4G (reuso panel)

## Aguas arriba

- Alimentacion por panel solar 6V + MPPT + 18650

**Option 1**

- SR04M Sensor ultrasonidos. MCU: A. Nano (R. Pico).
- MCU lee el sensor, calcula la distancia
- RS485, modo unidirectional cada 2 mins

**Option 2**

- Seedstudio RS485, en modo bidireccional
- TBC

## Referencias

- [DIY or BUY](https://www.youtube.com/watch?v=jriRW4rGQp4&t=224s)
- [how2electronics](https://how2electronics.com/modbus-rtu-with-raspberry-pi-pico-micropython/)
- Pedido AliExpress:
    - JSN-SR04T/AJ-SR04M Sensor de medición de distancia integrado a prueba de agua.
    - MPPT regulador de panel solar de 6V para batería de litio 3,7V 4,2V CN3791
    - RP2040 Raspbery Pico, USB-C + módulo RS485 TTL
 

![](fig/max485.png)
