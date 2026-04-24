# Deposito Water level

## Aguas abajo

La raspberry recibe un mensaje UART y lo muestra en un gauge

- PiZero + Max485 + 100m cable
- Pepephone + Router 4G

## Aguas arriba

- Alimentacion por panel solar 6V + MPPT + 18650
- DIY or BUY aleman: [video](https://www.youtube.com/watch?v=jriRW4rGQp4&t=224s)

### **Option 1**

- SR04M Sensor ultrasonidos. MCU: A. Nano (R. Pico).
- MCU lee el sensor, calcula la distancia y porcentaje
- Firmware modo unidirectional cada 120ms: see [code](main.ino)

![](fig/sensor.png)

Referencias
- Modo [auto](https://www.youtube.com/watch?v=n0hFgR4hYqY) del sensor
- Placa + MPPT Japo: [video](https://www.youtube.com/watch?v=pTtVe7P_lIc)

### **Option 2**

- Seedstudio RS485, en modo bidireccional

![](https://media-cdn.seeedstudio.com/media/catalog/product/cache/bb49d3ec4ee05b6f018e93f896b8a25d/1/-/1-101991041-rs485-750cm-ultrasonic-level-sensor-45font.jpg)

Referencias
- Protocolo ModBus RTU: [micropython](script.py)
- Modbus RTU micropython: [web](https://how2electronics.com/modbus-rtu-with-raspberry-pi-pico-micropython/)



## Pedido AliExpress

- JSN-SR04T/AJ-SR04M Sensor Ultrasonico: [datasheet](https://www.fabian.com.mt/viewer/42585/pdf.pdf)
- MPPT regulador de panel solar de 6V para batería de litio 3,7V 4,2V CN3791
- RP2040 Raspbery Pico, USB-C + módulo RS485 TTL

![](fig/max485.png)
