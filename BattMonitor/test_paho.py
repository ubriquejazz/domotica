# Beginners Guide To The Paho MQTT Python Client 
# 
import paho.mqtt.client as mqtt
import time

# 1. Configuration - Using your specific device ID
broker_address = "192.168.1.104"
#broker_address = "test.mosquitto.org" 
topic = "topic_esp"
valor = "23.7"
client_id = "RPi_e0d3738fd6ed" # Your unique hardware ID

# 2. Setup Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
client.username_pw_set("alumno", "clave123")

print(f"Conectando al broker: {broker_address}...")
client.connect(broker_address)

# 3. Publish and Wait
print(f"Enviando '{valor}' a '{topic}'...")
msg_info = client.publish(topic, valor, qos=1)

# This replaces time.sleep(2) - it waits only as long as necessary
#msg_info.wait_for_publish()
time.sleep(2)

client.disconnect()
print("Desconectado.")