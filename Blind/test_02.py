import RPi.GPIO as GPIO
import time

PIN_UP = 23
PIN_DW = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_UP, GPIO.OUT)
GPIO.setup(PIN_DW, GPIO.OUT)

def move_up(delay):
    print("Up")
    GPIO.output(PIN_UP, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(PIN_UP, GPIO.HIGH)

def move_down(delay):
    print("Down")
    GPIO.output(PIN_DW, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(PIN_DW, GPIO.HIGH)

try:
    GPIO.output(PIN_UP, GPIO.HIGH)
    GPIO.output(PIN_DW, GPIO.HIGH)
    while (True):
        move_down(2)
        print(".")
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()