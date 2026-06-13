import paho.mqtt.client as mqtt
from json import load
from relay import Rlay
from gpiozero import Button
from signal import pause
import sys

my_relay = Rlay(pin=16)
    
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

topic_pub = config["topic_thold"]   # Will resolve to "zero/thold"
topic_relay = config["topic_relay"]  # Will resolve to "zero/relay"
client_id = "RPi_e0d3738fd6ed"

# Map thresholds directly to pin numbers for cleaner logic
button_configs = {
    20: "4.7",
    21: "9.1"
}

# Keep track of active button objects
button_objects = []

# --- MQTT Logic ---
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"Connected! Listening for relay commands on: {topic_relay}")
        client.subscribe(topic_relay)
    else:
        print(f"Failed to connect. Code: {rc}")

def on_message(client, userdata, msg):
    command = msg.payload.decode().upper().strip()
    if command == "ON":
        my_relay.on()
    elif command == "OFF":
        my_relay.off()
    print(f"Relay command received [{command}]. Relay state is now: {my_relay.status()}")

def send_val(val_to_send):
    # Sends threshold data to "zero/thold"
    client.publish(topic_pub, str(val_to_send), qos=1)
    print(f"Sent new threshold value: {val_to_send} mA to {topic_pub}")

# --- Initialize MQTT ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
if mqtt_user and mqtt_pass:
    client.username_pw_set(mqtt_user, mqtt_pass)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(mqtt_server, 1883)
    client.loop_start()
except Exception as e:
    print(f"Could not connect to MQTT Broker at {mqtt_server}: {e}")
    sys.exit(1)

# --- Initialize Buttons ---
# We write an explicit helper generator to prevent lambda scope bleed
def make_callback(value):
    return lambda: send_val(value)

for pin, val in button_configs.items():
    btn = Button(pin)
    btn.when_pressed = make_callback(val)
    button_objects.append(btn)
    print(f"Button on GPIO {pin} configured to send threshold: {val} mA")

print(f"System Ready. Send 'ON' or 'OFF' to {topic_relay}")

try:
    pause()
except KeyboardInterrupt:
    print("\nCleaning up and exiting... (gpiozero handles pin cleanup automatically)")