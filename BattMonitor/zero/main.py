import paho.mqtt.client as mqtt
from json import load
from relay import Rlay
from gpiozero import Button
from signal import pause

my_relay = Rlay(pin=16)
    
# --- Config ---
with open("config.json", "r") as f:
    config = load(f)
    f.close()

mqtt_server = config["mqtt_server"]
mqtt_user = config["mqtt_user"]
mqtt_pass = config["mqtt_pass"]

topic_data = config["topic_thold"]
topic_relay = config["topic_relay"]
client_id = "RPi_e0d3738fd6ed"

buttons = {
    "A": Button(20),
    "B": Button(21)
}

values = {
    "A": "4.7", 
    "B": "9.1"
}

# --- MQTT Logic ---
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected! Listening for relay commands...")
        client.subscribe(topic_relay)
    else:
        print(f"Failed to connect. Code: {rc}")

def on_message(client, userdata, msg):
    command = msg.payload.decode().upper()
    if command == "ON":
        my_relay.on()
    elif command == "OFF":
        my_relay.off()
    print(f"Relay is now:", my_relay.status())

def send_val(label):
    val = values[label]
    client.publish(topic_data, val, qos=1)
    print(f"Sent {val} to {topic_data}")

# --- Initialize ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
client.username_pw_set(mqtt_user, mqtt_pass)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server, 1883)
client.loop_start()

# Link the 4 buttons
for label, btn in buttons.items():
    # We use 'l=label' to make sure the button remembers its OWN name
    btn.when_pressed = lambda l=label: send_val(l)
    print(f"Button {label} configured to send {values[label]}")

print(f"System Ready. Send 'ON' or 'OFF' to {topic_relay}")
try:
    pause()
except KeyboardInterrupt:
    print("\nCleaning up GPIO pins...")
    GPIO.cleanup()