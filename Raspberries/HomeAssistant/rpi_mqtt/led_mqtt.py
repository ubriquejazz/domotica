import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Define GPIO Pins for Relays
BLIND_UP = 23
BLIND_DOWN = 24
SW1 = 9
SW2 = 11
DURATION = 20

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLIND_UP, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BLIND_DOWN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# MQTT Configuration
MQTT_BROKER = "172.16.1.114"  # Replace with your Home Assistant IP
MQTT_PORT = 1883
MQTT_TOPIC_BLIND = "azotea/blind"
MQTT_STATE_TOPIC = "azotea/blind/state"
MQTT_USER = "mqtt"  # Replace with your MQTT user
MQTT_PASSWORD = "mqtt"

def move_up(delay):
    GPIO.output(BLIND_DOWN, GPIO.HIGH)  # Ensure DOWN is off
    GPIO.output(BLIND_UP, GPIO.LOW)     # Activate UP relay
    time.sleep(delay)
    GPIO.output(BLIND_UP, GPIO.HIGH)    # Stop the motor

def move_down(delay):
    GPIO.output(BLIND_UP, GPIO.HIGH)    # Ensure UP is off
    GPIO.output(BLIND_DOWN, GPIO.LOW)   # Activate DOWN relay
    time.sleep(delay)
    GPIO.output(BLIND_DOWN, GPIO.HIGH)  # Stop the motor

# Callback function for received messages
def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip().upper()  # Normalize input

    if payload == "UP":
        move_up(DURATION)

    elif payload == "DOWN":
        move_down(DURATION)

    elif payload == "STOP":
        GPIO.output(BLIND_UP, GPIO.HIGH)
        GPIO.output(BLIND_DOWN, GPIO.HIGH)

    else:
        print(f"Unknown command: {payload}")

# Publish the current state
def publish_state(client, state):
    print(f"Publishing state: {state}")
    client.publish(MQTT_STATE_TOPIC, state, retain=True)

def button_up():
    move_up(DURATION)

def button_down():
    move_down(DURATION)

# SW Setup
GPIO.add_event_detect(SW1, GPIO.FALLING, callback=button_up) 
GPIO.add_event_detect(SW2, GPIO.FALLING, callback=button_down) 

# MQTT Setup
time.sleep(20) # Wait for the network to be ready
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC_BLIND)

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
print("End of the program")