import time
import machine
import dht
import ujson
from umqtt.simple import MQTTClient

# time.ticks_ms() equivale a millis() en Arduino
start_time = time.ticks_ms()

# --- Configuración de Pines y Periféricos ---
LED = machine.Pin(2, machine.Pin.OUT, value=1)  # Pin D4 (GPIO2 en ESP8266 de forma nativa)
sensor_pin = machine.Pin(0)                     # Pin D3 (GPIO0 en ESP8266 de forma nativa)
sensor = dht.DHT22(sensor_pin)

# --- Configuración de Tiempos ---
SLEEP_TIME_MIN = 10

# --- Filosofía de Conexión MQTT ---
def connect_and_subscribe():
    # Creamos el cliente usando los datos heredados de boot.py
    client = MQTTClient(boot.client_id, boot.mqtt_server, port=1883)
    client.connect()
    print('Connected to %s MQTT broker' % boot.mqtt_server)
    return client

def restart_and_reconnect():
    print('Failed to connect or network error. Reconnecting via reset...')
    # Parpadeo rápido de aviso antes de reiniciar si falla el Broker
    for _ in range(10):
        LED.value(not LED.value())
        time.sleep(0.1)
    machine.reset()

# --- Intento de Conexión Inicial ---
try:
    client = connect_and_subscribe()
except OSError as e:
    print("MQTT Connection failed:", e)
    restart_and_reconnect()

# --- Lectura de Sensor y Envío MQTT ---
try:
    # El DHT22 necesita un pequeño delay antes de medir la primera vez tras arrancar
    time.sleep(0.5) 
    sensor.measure()
    
    t = sensor.temperature()
    h = sensor.humidity()
    
    print(f"Humedad: {h} % \t Temperatura: {t} *C")
    
    # Formatear el payload en JSON tal como lo hacía ArduinoJson
    payload = {
        "temp": t,
        "hum": h
    }
    msg_json = ujson.dumps(payload).encode('utf-8')
    
    # Publicar datos y cerrar sesión limpiamente
    client.publish(b"home/room/status", msg_json)
    client.disconnect()
    
except Exception as e:
    print("Error leyendo el sensor o publicando:", e)

# --- Cálculo de compensación de tiempo y Deep Sleep ---
# Calculamos cuánto tiempo hemos tardado en conectar y medir para restarlo del sueño
elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
sleep_time_ms = (SLEEP_TIME_MIN * 60 * 1000) - elapsed_time

print(f"Tiempo despierto: {elapsed_time} ms. Durmiendo por: {sleep_time_ms} ms.")

# Desconectar interfaz de red explícitamente antes de dormir (equivale a WiFi.disconnect())
boot.station.active(False)

# Entrar en ciclo Deep Sleep (En ESP8266 el parámetro se pasa en milisegundos)
machine.deepsleep(max(10, sleep_time_ms))