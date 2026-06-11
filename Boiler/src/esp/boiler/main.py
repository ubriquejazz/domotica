import time
import machine
import ujson
from umqtt.simple import MQTTClient

RELAY = machine.Pin(0, machine.Pin.OUT, value=1)  # Inicializa en HIGH
LED = machine.Pin(2, machine.Pin.OUT, value=1)    # Inicializa en HIGH

with open("config.json", "r") as f:
    config = ujson.load(f)
    f.close()

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
    client = MQTTClient(client_id, mqtt_server, port=1883)
    
    client.set_callback(on_message)
    client.connect()
    print('Connected to %s MQTT broker' % boot.mqtt_server)
    
    # Nos suscribimos a los tópicos necesarios
    client.subscribe(topic_sub)
    client.subscribe(b"home/relay/get")
    
    # Publicamos anuncio de conexión exitosa
    client.publish(topic_pub, b"(Re)Connected")
    return client



try:
    client = connect_and_subscribe()
except Exception as error:
    print("Failed to handshake broker instance. Initializing soft boot reset window...", error)
    time.sleep(10)
    machine.reset()

last_status_broadcast = 0
broadcast_interval = 10  # Enviar estado cada 10 segundos de forma cíclica

while True:
    try:
        client.check_msg()
        
        if (time.time() - last_status_broadcast) > broadcast_interval:
            estado = "ON" if RELAY.value() == 0 else "OFF"
            payload = {
                "relay_status": estado,
                "uptime_s": time.time()
            }
            msg_json = ujson.dumps(payload).encode('utf-8')
            
            client.publish(topic_pub, msg_json)
            last_status_broadcast = time.time()
            
        time.sleep(0.1) # Pequeño respiro para el procesador
        
    except OSError as e:
        print("Network error caught:", e)
        restart_and_reconnect()