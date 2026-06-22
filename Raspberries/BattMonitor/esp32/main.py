import ujson
from ina3221 import INA3221

try:
    with open("config.json", "r") as f:
        config = ujson.load(f)
except OSError:
    print("Error: config.json file not found!")
    machine.reset()

client_id = "esp32_ina3221"
mqtt_server = config["mqtt_server"]
mqtt_user = config.get("mqtt_user", "")
mqtt_pass = config.get("mqtt_pass", "")
topic_pub = config["topic_esp"]  # Will resolve to "esp/ina"

def connect_and_subscribe():
    if mqtt_user and mqtt_pass:
        client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
    else:
        client = MQTTClient(client_id, mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker' % mqtt_server)
    return client

def restart_and_reconnect():
    print('Reconnecting in 10 seconds...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

sensor = INA3221()
last_sensor_reading = 0
readings_interval = 6
count = 0

while True:
    try:
        client.check_msg()
        current_time = time.time()
        
        if (current_time - last_sensor_reading) > readings_interval:     
            # Get current in Amperes, convert to mA for the web frontend
            current_mA = sensor.get_current(1) * 1000
            
            # The web dashboard parses the reading, and 'count' as the timestamp
            payload = {
                "temp": current_mA,
                "count": count
            }
            
            msg = ujson.dumps(payload).encode('utf-8')      
            client.publish(topic_pub, msg)
            print("Sent to Web Dashboard:", payload)
            
            last_sensor_reading = current_time
            count += 1
            
    except OSError as e:
        print("Network error caught:", e)
        restart_and_reconnect()
        
    time.sleep(0.1)