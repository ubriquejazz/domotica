import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'Flybox_3AE8'
password = '34823743'

mqtt_server = '192.168.1.104'
client_id = ubinascii.hexlify(machine.unique_id())

led = machine.Pin(2, machine.Pin.OUT, value=1)

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

led.value(0) # Apagar LED (Modo activo bajo en configuración exitosa)
print('Connection successful')
print(station.ifconfig())
