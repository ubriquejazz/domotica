import ujson
from ina3221 import INA3221

client_id = "esp32_ina3221"

with open("config.json", "r") as f:
    config = ujson.load(f)
    f.close()

mqtt_server = config["mqtt_server"]
mqtt_user = config["mqtt_user"]
mqtt_pass = config["mqtt_pass"]
topic_pub = config["topic_esp"]
# b'sensor/temperature'  # Changed to a more descriptive topic

def connect_and_subscribe():
  global client_id, mqtt_server
  #client = MQTTClient(client_id, mqtt_server)
  client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
  #client.set_callback(on_message)
  client.connect()
  print('Connected to %s MQTT broker' % mqtt_server)
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

sensor = INA3221();
last_sensor_reading = 0
readings_interval = 6
count = 0

while True:
  try:
    client.check_msg()
    if (time.time() - last_sensor_reading) > readings_interval:     
      simulated_temp = 100 * sensor.get_current(1)
      
      msg = b'%d' % simulated_temp  
      payload = {
        "temp": simulated_temp,
        "count": count}
      msg = ujson.dumps(payload).encode('utf-8')      
      #msg = b'Hello #%d' % count      
      client.publish(topic_pub, msg)
      last_sensor_reading = time.time()
      count += 1
  except OSError as e:
    print("Network error caught:", e)
    restart_and_reconnect()
