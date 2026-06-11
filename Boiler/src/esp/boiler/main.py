import time
import ujson

with open("config.json", "r") as f:
    config = ujson.load(f)
    f.close()

pin = int(config['relay_pin'])
broadcast_interval = int(config['update_interval_min'])
RELAY = machine.Pin(pin, machine.Pin.OUT, value=1)  # Inicializa en HIGH

MQTT_SERVER = config["mqtt_server"]
MQTT_USER = config.get("mqtt_user", "")
MQTT_PASS = config.get("mqtt_pass", "")

T_RELAY_SET = config["topic_relay_set"]         # "home/relay/set"
T_RELAY_STATUS = config["topic_relay_status"]   # "home/relay/status"

def on_message(topic, msg):
    topic_str = topic.decode("utf-8")
    payload_str = msg.decode("utf-8").strip()
    
    print("Received message -> [{}]: {}".format(topic_str, payload_str))

    if topic_str == T_RELAY_SET:
        # Active-Low logic mapping matching boiler.cpp requirements:
        # "1" or "ON"  -> Drop Pin to 0V (GND) to activate the relay contactor
        # "0" or "OFF" -> Drive Pin to 3.3V (VCC) to turn off the heating loop
        if payload_str == "1" or payload_str.upper() == "ON":
            LED.value(1)       # Status Indicator ON
            RELAY.value(0)     # ACTIVE LOW: Relay closed circuit (Heater ON)
            print("Boiler Circuit Status -> ENERGIZED")
        elif payload_str == "0" or payload_str.upper() == "OFF":
            LED.value(0)       # Status Indicator OFF
            RELAY.value(1)     # ACTIVE LOW: Relay open circuit (Heater OFF)
            print("Boiler Circuit Status -> DE-ENERGIZED")
            
        # Immediately confirm current physical state back to the telemetry status path
        current_state = "ON" if RELAY.value() == 0 else "OFF"
        client.publish(T_RELAY_STATUS, current_state, retain=True)


def connect_and_subscribe():
    client_id = "esp32-boiler-actuator"
    
    # Configure parameter arrays safely supporting empty security configurations
    user_auth = MQTT_USER if MQTT_USER != "" else None
    pass_auth = MQTT_PASS if MQTT_PASS != "" else None
    
    client = MQTTClient(
        client_id=client_id, 
        server=MQTT_SERVER, 
        user=user_auth, 
        password=pass_auth,
        keepalive=60
    )
    
    client.set_callback(on_message)
    client.connect()
    print("Connected to Mosquitto Broker at {} successfully.".format(MQTT_SERVER))
    
    # Register subscription filters matching the structural infrastructure topic contracts
    client.subscribe(T_RELAY_SET)
    print("Subscribed to command channel: {}".format(T_RELAY_SET))
    
    # Announce presence on bootup
    initial_state = "OFF" if RELAY.value() == 1 else "ON"
    client.publish(T_RELAY_STATUS, initial_state, retain=True)
    return client

try:
    client = connect_and_subscribe()
except Exception as error:
    print("Failed to handshake broker instance. Initializing soft boot reset window...", error)
    time.sleep(10)
    machine.reset()

last_status_broadcast = 0
while True:
    try:
        client.check_msg()
        
        if (time.time() - last_status_broadcast) > broadcast_interval:
            current_state = "ON" if RELAY.value() == 0 else "OFF"
            client.publish(T_RELAY_STATUS, current_state, retain=True)

            last_status_broadcast = time.time()
            
        time.sleep(0.1) # Pequeño respiro para el procesador
        
    except OSError as e:
        print("Network error caught:", e)
        restart_and_reconnect()