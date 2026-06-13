import paho.mqtt.client as mqtt
from json import load
from signal import pause
import sys, serial
    
# --- Config ---
try:
    with open("config.json", "r") as f:
        config = load(f)
except FileNotFoundError:
    print("Error: config.json not found on this Raspberry Pi!")
    sys.exit(1)

mqtt_server = config["mqtt_server"]
mqtt_user = config["mqtt_user"]
mqtt_pass = config["mqtt_pass"]

topic_pub = config["topic_temp"]  # Will resolve to "tanque/ciclos"
client_id = "RPi_e0d3738fd6ed"

# Configuración del Puerto Serie (ajusta el puerto según tu Raspberry)
# Para la RP2040 conectada por USB suele ser /dev/ttyACM0
SER_PORT = "/dev/ttyACM0" 
BAUD_RATE = 115200

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
if mqtt_user and mqtt_pass:
    client.username_pw_set(mqtt_user, mqtt_pass)

try:
    client.connect(mqtt_server, 1883)
    client.loop_start()
except Exception as e:
    print(f"Could not connect to MQTT Broker at {mqtt_server}: {e}")
    sys.exit(1)

try:
    ser = serial.Serial(SER_PORT, BAUD_RATE, timeout=1)
    print("Leyendo datos de la RP2040...")
    
    while True:
        if ser.in_waiting > 0:
            # Leer la línea que envía la RP2040
            linea = ser.readline().decode('utf-8').strip()
            
            if linea.isdigit(): # Asegurarnos 
                payload = {
                    "temp": int(linea),
                    "count": count
                }
                
                msg = ujson.dumps(payload).encode('utf-8')      
                client.publish(topic_pub, msg)
                print("Sent to Web Dashboard:", payload)
                count += 1
            
                
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Cerrando programa...")
    ser.close()
    client.loop_stop()
