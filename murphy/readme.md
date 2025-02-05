# Murphy

## Home assistant (hass)

- [YAML files in HASS](https://www.youtube.com/watch?v=lKDcnfaX7O8&t=333s)
- Install the MQTT Client on the RPi1 (paho-mqtt)
- Python script called led_mqtt
- Test of the setup designed by Ardubrico

## Web Interface Design

1. LED Status Indicator:
    Green = ON; Red = OFF
1. Live Data Display:
    Sensor readings (e.g., temperature, humidity).

### Arduino

| Command | Topic |
| ------- | ----- |
| LEDON | Enciende el LED interno| 
| LEDOFF | Apaga el LED interno| 
| STATUS | Muestra el estado del LED| 
| GET_TEMP | Obtiene la temperatura actual| 

### Manual de usuario

1. Ejecuta el servidor:

    python app.py

1. Obtener temperatura:
    
        curl http://localhost:5000/get-temp

1. Encender el LED:

        curl -X POST -H "Content-Type: application/json" -d '{"action": "ON"}' http://localhost:5000/toggle-led

1. Verificar estado del LED:

        curl http://localhost:5000/led-status

