# Design web interfaces for IoT devices to monitor and control hardware

**Objectives**
- Developed user-friendly dashboards with real-time data visualization using Flask
- Enabled secure control mechanisms over MQTT and WebSocket protocols to interact with hardware.
- Integrated Grafana to provide advanced monitoring and analytical insights for hardware performance metrics.

## Arduino (main.ino)

| Command | Topic |
| ------- | ----- |
| LEDON | Enciende el LED interno| 
| LEDOFF | Apaga el LED interno| 
| STATUS | Muestra el estado del LED| 
| GET_TEMP | Obtiene la temperatura actual| 

## Web Interface Design

1. LED Status Indicator:
    Green = ON; Red = OFF
1. Live Data Display:
    Sensor readings (e.g., temperature, humidity).

## Manual de usuario

1. Ejecuta el servidor:

    python app.py

1. Obtener temperatura:
    
        curl http://localhost:5000/get-temp

1. Encender el LED:

        curl -X POST -H "Content-Type: application/json" -d '{"action": "ON"}' http://localhost:5000/toggle-led

1. Verificar estado del LED:

        curl http://localhost:5000/led-status
