# Water level (ultrasonic)

Primero vemos lo que se instala en el deposito (aguas arribas):

- Placa + MPPT (ver [video](https://www.youtube.com/watch?v=pTtVe7P_lIc) en japonés)

- Sensor ultrasonidos AJ-SR04M (R19 horizontal): 
    - Modo [auto](https://www.youtube.com/watch?v=n0hFgR4hYqY), [datasheet](https://www.fabian.com.mt/viewer/42585/pdf.pdf)

- Control y envio por MSP430F2013 y RS485

### Implementation (aguas abajo)

![](fig/garaje.png)


- Step-down a 5V (USB) de DollaTek:
  - **Entrada:** Conectado directamente a los 24V de tu batería.
  - **Salida USB:** hacia la **Raspberry Pi** para darle energía de forma segura.
  - **Salida bornas:** pin **VBUS** (o VSYS) de placa RP2040. El regulador interno se encargará de bajar esos 5V a los 3.3V que necesita para funcionar. 

### MQTT client (paho_main.py on RPi)

```
crontab -e
@reboot sleep 30; cd /path_to_code/; /usr/bin/python3 paho_main.py
```

Suponemos que en esos 30s le ha dado tiempo de iniciar el interfaz WiFi, antes de lanzar los clientes MQTT. Si no, vamos a lanzar el siguiente comando:
```
cd /path_to_code; screen
python3 paho_main.py
```
You can detach from the screen session by pressing `Ctrl+a D`. To come back, use `screen -r` 


### MQTT client (html/functions.js on RPi)

Paho is web browser based and uses WebSockets to connect to brokers (you don’t need to deal with the possibility of port 1833 being blocked)


### Comunicaciones

| Aguas arriba (20 mA) | Aguas abajo (200 mA) |
|----------------------|----------------------|
| ![](fig/rs3485.PNG) | ![](fig/max485.png) |
| Módulo **MAX3485** @ 3V3  <br />half duplex, DE = RE# active high for TX | Módulo **MAX485** @ 5V; full duplex, DE active high, RE# active low (viceversa) |

### Consumos

| Concepto | Potencia |
|--------|-----------|
| RS485 transceiver | 0,5 W |
| DollaTek buck converter | 0,1 W |
| RP2040 + Pantalla LCD | 5V * 0.2A = 1W |
| Raspberry Pi4 | 5V * 2.0A = 10W |
| Router Flybox | 12V * 1A = 12W |
|  |  |
| Baterias tudor (Pb Acido) | Tudor 24V @ 90Ah / 2= 1080 Wh |
| Total 24W | 40h de autonomia |

### Alternatives

Opcion 1 - La raspberry recibe el mensaje UART y lo muestra en Javascript

Opcion 2 - home-assistant

- Este [esphome](https://esphome.io/components/sensor/jsn_sr04t/) es para el ultrasonido SR04M-2

Opcion 3 - LCD intermedio 

- RP040 para poder mostrar el nivel en un LCD



### Referencias

- DIY or BUY aleman: [video](https://www.youtube.com/watch?v=jriRW4rGQp4&t=224s)
- I2C LCD [library](https://github.com/DIYables/DIYables_MicroPython_LCD_I2C) for ESP32, Pico, etc.
- MPPT regulador de panel solar de 6V para batería de litio 3,7V 4,2V [CN3791](https://www.laskakit.cz/user/related_files/dse-cn3791.pdf)
- **Implementation (aguas arriba)**: [codigo](https://github.com/ubriquejazz/micros/blob/master/MSP430/deposito/main_lpm.c) en repositorio de micros/MSP430


| Name | Comments |
|------|----------|
| AJ-SR04M () | R19 horizontal |
| SR04M-2 | R19 vertical |
| Rs485 | ![](fig/max485.png) |