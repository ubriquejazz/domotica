# Deposito Water level

Vemos lo que se instala en el deposito (aguas arribas). Para la instalación en la casa, ver aguas [abajo](a_abajo.md)...

- Placa + MPPT (ver [video](https://www.youtube.com/watch?v=pTtVe7P_lIc) en japonés)
- MSP430F2013 + Sensor ultrasonidos 
    - Modo [auto](https://www.youtube.com/watch?v=n0hFgR4hYqY) 
    - AJ-SR04M (R19 horizontal): [datasheet](https://www.fabian.com.mt/viewer/42585/pdf.pdf)
    
- Comunicación RS485 unidireccional
    - Módulo MAX3485 @ 3V3 (half duplex, aguas arriba)
    - Módulo MAX485 @ 5V: DE active high, RE# active low (aguas abajo)

| Aguas arriba (20 mA) | Aguas abajo (200 mA) |
|----------------------|----------------------|
| ![](fig/rs3485.PNG) | ![](fig/max485.png) |

DE = RE# active high for TX (MAX3485)

## Material

- MPPT regulador de panel solar de 6V para batería de litio 3,7V 4,2V CN3791

| Opcion Barata | Opcion integrada|
|----------------------|----------------------|
| AJ-SR04M (R19 horizontal) | ![Seedstudio](https://media-cdn.seeedstudio.com/media/catalog/product/cache/bb49d3ec4ee05b6f018e93f896b8a25d/1/-/1-101991041-rs485-750cm-ultrasonic-level-sensor-45font.jpg)|
| SR04M-2  (R19 vertical) | Ver [protocolo](https://how2electronics.com/modbus-rtu-with-raspberry-pi-pico-micropython/) ModBus RTU y script en **esp/modbus.py** |
