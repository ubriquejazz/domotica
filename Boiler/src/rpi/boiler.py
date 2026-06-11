import logging
import json
import os
import time as t
from datetime import datetime
import paho.mqtt.client as mqtt # type: ignore
import Adafruit_DHT # type: ignore
from controller import *

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
    set_flag = False
    if message.topic == "home/params/set/start_time":
        param = str(message.payload.decode("utf-8"))
        client.publish("home/params/status/start_time", param)
        start = datetime.strptime(param, "%H:%M")
        controller.set_time_start(start.time())
        logging.info("Set Param Time Start: " + param + "h")
        dic["time_start"] = param
        set_flag = True
    elif message.topic == "home/params/set/stop_time":
        param = str(message.payload.decode("utf-8"))
        client.publish("home/params/status/stop_time", param)
        stop = datetime.strptime(param, "%H:%M")
        controller.set_time_stop(stop.time())
        logging.info("Set Param Time Stop: " + param + "h")
        dic["time_stop"] = param
        set_flag = True
    elif message.topic == "home/params/set/user_temp":
        param = float(message.payload.decode("utf-8"))
        client.publish("home/params/status/user_temp", param)
        controller.set_user_temp(param)
        logging.info("Set Param User Temp: " + str(param) + "ºC")
        dic["user_temp"] = param
        set_flag = True
    elif message.topic == "home/params/set/back_temp":
        param = float(message.payload.decode("utf-8"))
        client.publish("home/params/status/back_temp", param)
        controller.set_back_temp(param)
        logging.info("Set Param Back Temp: " + str(param) + "ºC")
        dic["back_temp"] = param
        set_flag = True
    elif message.topic == "home/params/get":
        print("Web user!")
        client.publish("home/params/status/curr_temp", "{0:0.1f}".format(temperature))
        client.publish("home/params/status/start_time", controller.get_time_start().strftime("%H:%M"))
        client.publish("home/params/status/stop_time", controller.get_time_stop().strftime("%H:%M"))
        client.publish("home/params/status/user_temp", controller.get_user_temp())
        client.publish("home/params/status/back_temp", controller.get_back_temp())
    elif message.topic == "home/relay/status":
        print("ESP access!")
        logging.info("Boiler Feedback: " + str(message.payload.decode("utf-8")))
        # do nothing, the esp32 is answering
    if set_flag == True:
        conf_str = json.dumps(dic, indent=4)
        with open('conf.json', 'w') as f:
            f.write(conf_str)
            f.close()

print("**************** Automatic Boiler program ***************")
print(dic)
# Configuration
UPDATE_MINUTE = 2
DHT_SENSOR = 11
DHT_PIN_DATA = 4

# Subscribe
client = mqtt.Client("RPi")
client.connect("localhost")
client.subscribe("home/relay/status")
client.subscribe("home/params/set/#")
client.subscribe("home/params/get")
#client.subscribe("home/room/status")
client.on_message = on_message
client.loop_start()

# Log file
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
now = datetime.now()
now_str = now.strftime("%Y%m%d_%H%M")
log_file = "./logs/boiler_" + now_str + ".log"
logging.basicConfig(filename = log_file, level = logging.INFO)
print("- File " + log_file + " created")

# Main loop
while True:

    # Read sensor and time (first read is deprecated)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN_DATA)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN_DATA)
    now = datetime.now()
    log_str = now.strftime("%Y/%m/%d_%H:%M:%S")

    if humidity is not None and temperature is not None:
        log_str += " Temp={0:0.1f}ºC Hum={1:0.1f}%".format(temperature, humidity)
        client.publish("home/params/status/curr_temp", "{0:0.1f}".format(temperature))
        # Control
        signal = controller.control(temperature, now.time())
        log_str += " Target={0:0.1f}ºC".format(controller.get_target_temp())
        if signal == ControlResult.TURN_ON:
            client.publish("home/relay/set", 1)
            log_str += " ON"
            boiler_st = True
        elif signal == ControlResult.TURN_OFF:
            client.publish("home/relay/set", 0)
            log_str += " OFF"
            boiler_st = False
    else:
        log_str += " Failed to retrieve data from sensor"

    # Print
    logging.info(log_str)

    # Wait
    while True:
        t.sleep(1)
        now = datetime.now()
        if ((now.minute % UPDATE_MINUTE) == 0) and (now.second == 0):
            break