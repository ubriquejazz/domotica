import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Define GPIO Pins for Relays
BLIND_UP = 23
BLIND_DOWN = 24

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLIND_UP, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BLIND_DOWN, GPIO.OUT, initial=GPIO.HIGH)

# MQTT Configuration
MQTT_BROKER = "172.16.1.109"  # Replace with your Home Assistant IP
MQTT_PORT = 1883
MQTT_TOPIC_BLIND = "home/blind"
MQTT_USER = "mqtt_user"  # Replace with your MQTT user
MQTT_PASSWORD = "your_password"

def move_up(delay):
    print("Up")
    GPIO.output(BLIND_DOWN, GPIO.HIGH)  # Ensure DOWN is off
    GPIO.output(BLIND_UP, GPIO.LOW)     # Activate UP relay
    time.sleep(delay)
    GPIO.output(BLIND_UP, GPIO.HIGH)    # Stop the motor

def move_down(delay):
    print("Down")
    GPIO.output(BLIND_UP, GPIO.HIGH)    # Ensure UP is off
    GPIO.output(BLIND_DOWN, GPIO.LOW)   # Activate DOWN relay
    time.sleep(delay)
    GPIO.output(BLIND_DOWN, GPIO.HIGH)  # Stop the motor

# Callback function for received messages
def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip().upper()  # Normalize input

    if payload == "UP":
        print("Raising the blind ⬆️")
        move_up(2)

    elif payload == "DOWN":
        print("Lowering the blind ⬇️")
        move_down(2)

    elif payload == "STOP":
        print("Stopping the blind ⏹")
        GPIO.output(BLIND_UP, GPIO.HIGH)
        GPIO.output(BLIND_DOWN, GPIO.HIGH)

    else:
        print(f"Unknown command: {payload}")

# MQTT Setup
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC_BLIND)

# Start MQTT loop
client.loop_forever()
