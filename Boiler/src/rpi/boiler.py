import logging
import json
import os, sys
import time as t
from datetime import datetime
import paho.mqtt.client as mqtt # type: ignore
import Adafruit_DHT # type: ignore
from controller import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

with open('config.json', 'r') as f:
    infra_config = json.load(f)
    f.close()

with open('bolier.json', 'r') as f:
    user_config = json.load(f)
    f.close()

controller = Controller.fromdict(user_config)
boiler_st = None
current_temperature = None

# ---- 2. Map Constants from config.json ----
MQTT_SERVER   = infra_config["mqtt_server"]
MQTT_PORT     = infra_config.get("mqtt_port", 1883)
MQTT_USER     = infra_config.get("mqtt_user", "")
MQTT_PASS     = infra_config.get("mqtt_pass", "")

T_RELAY_SET   = infra_config["topic_relay_set"]
T_RELAY_STATUS= infra_config["topic_relay_status"]
T_PARAMS_GET  = infra_config["topic_params_get"]
PREFIX_SET    = infra_config["topic_params_set_prefix"]      # "home/params/set/"
PREFIX_STATUS = infra_config["topic_params_get_prefix"]      # "home/params/status/"

UPDATE_INTERVAL = infra_config.get("update_interval_seconds", 120)

def on_message(client, userdata, message):
    global current_temperature
    set_flag = False
    topic = message.topic
    payload = message.payload.decode("utf-8").strip()

    try:
        if topic == f"{PREFIX_SET}start_time":
            client.publish(f"{PREFIX_STATUS}start_time", payload, retain=True)
            start = datetime.strptime(payload, "%H:%M")
            controller.set_time_start(start.time())
            user_config["time_start"] = payload
            set_flag = True

        elif topic == f"{PREFIX_SET}stop_time":
            client.publish(f"{PREFIX_STATUS}stop_time", payload, retain=True)
            stop = datetime.strptime(payload, "%H:%M")
            controller.set_time_stop(stop.time())
            user_config["time_stop"] = payload
            set_flag = True

        elif topic == f"{PREFIX_SET}user_temp":
            val = float(payload)
            client.publish(f"{PREFIX_STATUS}user_temp", val, retain=True)
            controller.set_user_temp(val)
            user_config["user_temp"] = val
            set_flag = True

        elif topic == f"{PREFIX_SET}back_temp":
            val = float(payload)
            client.publish(f"{PREFIX_STATUS}back_temp", val, retain=True)
            controller.set_back_temp(val)
            user_config["back_temp"] = val
            set_flag = True

        elif topic == T_PARAMS_GET:
            # Synchronize loading views with a clean parameter state dump
            if current_temperature is not None:
                client.publish(f"{PREFIX_STATUS}curr_temp", f"{current_temperature:.1f}")
            client.publish(f"{PREFIX_STATUS}start_time", controller.get_time_start().strftime("%H:%M"))
            client.publish(f"{PREFIX_STATUS}stop_time", controller.get_time_stop().strftime("%H:%M"))
            client.publish(f"{PREFIX_STATUS}user_temp", controller.get_user_temp())
            client.publish(f"{PREFIX_STATUS}back_temp", controller.get_back_temp())

        # CRITICAL FIX: Only modify and write boiler.json, leaving config.json intact
        if set_flag:
            with open(USER_CONFIG_PATH, 'w') as f:
                json.dump(user_config, f, indent=4)
            recalculate_heating()

    except Exception as e:
        logging.error(f"Error handling UI event on topic {topic}: {e}")
        
def recalculate_heating():
    """Evaluates current room telemetry against active targets immediately."""
    global boiler_st
    if current_temperature is None:
        return

    now = datetime.now()
    signal = controller.control(current_temperature, now.time())
    target = controller.get_target_temp()
    
    log_str = f"{now.strftime('%Y/%m/%d_%H:%M:%S')} Temp: {current_temperature:.1f}°C, Target: {target:.1f}°C"

    if signal == ControlResult.TURN_ON:
        client.publish(T_RELAY_SET, 1, qos=1)
        logging.info(f"{log_str} | Command -> TURN_ON")
        boiler_st = True
    elif signal == ControlResult.TURN_OFF:
        client.publish(T_RELAY_SET, 0, qos=1)
        logging.info(f"{log_str} | Command -> TURN_OFF")
        boiler_st = False

dht_pin_attr = getattr(board, f"D{infra_config['dht_pin']}")
dht_device = adafruit_dht.DHT11(dht_pin_attr)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "RPi_Boiler_Core")
if MQTT_USER and MQTT_PASS:
    client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_message = on_message


# Subscribe
try:
    client.connect(MQTT_SERVER, MQTT_PORT)
    client.subscribe(T_RELAY_STATUS)
    client.subscribe(f"{PREFIX_SET}#")
    client.subscribe(T_PARAMS_GET)
    client.loop_start()
except Exception as e:
    print(f"Network Fault linking Broker: {e}")
    sys.exit(1)

# Log file
now_str = datetime.now().strftime("%Y%m%d_%H%M")
logging.basicConfig(filename=os.path.join(LOG_DIR, f"boiler_{now_str}.log"), level=logging.INFO)

print("**************** Automatic Boiler Program Running ***************")

last_sensor_read = 0

try:
    while True:
        current_time = t.time()
        
        # Non-blocking evaluation window check
        if (current_time - last_sensor_read) >= UPDATE_INTERVAL:
            try:
                humidity = dht_device.humidity
                temp = dht_device.temperature

                if humidity is not None and temp is not None:
                    current_temperature = float(temp)
                    client.publish(f"{PREFIX_STATUS}curr_temp", f"{current_temperature:.1f}", retain=True)
                    recalculate_heating()
            except RuntimeError as error:
                logging.warning(f"DHT background read noise: {error.message}")
            
            last_sensor_read = current_time

        t.sleep(0.5)

except KeyboardInterrupt:
    print("\nClosing background threads...")
    dht_device.exit()