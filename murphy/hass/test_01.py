import RPi.GPIO as GPIO
import time

RELAY01 = 23
RELAY02 = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY01, GPIO.OUT)
GPIO.setup(RELAY02, GPIO.OUT)

def releON(id):
    if id == 1:
        GPIO.output(RELAY01, GPIO.LOW)
    elif id == 2:
        GPIO.output(RELAY02, GPIO.LOW)
    
def releOFF(id):
    if id == 1:
        GPIO.output(RELAY01, GPIO.HIGH)
    elif id == 2:
        GPIO.output(RELAY02, GPIO.HIGH)
    else:
        GPIO.output(RELAY01, GPIO.HIGH)
        GPIO.output(RELAY02, GPIO.HIGH)

try:
    releOFF(0)
    while (True):
        print(".")
        releON(1)
        time.sleep(2)
        releOFF(1)

        print(".")
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()