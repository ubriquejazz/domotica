import RPi.GPIO as GPIO
import time
import sys

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

if __name__ == "__main__":

    if len(sys.argv) != 2 or sys.argv[1] not in ["up", "down"]:
        print("Usage: python test_blind.py [up|down]")
        sys.exit(1)

    direction = sys.argv[1]
    try:
        GPIO.output(PIN_UP, GPIO.HIGH)
        GPIO.output(PIN_DW, GPIO.HIGH)
        while (True):            
            if direction == "up": move_up(2)
            else: move_down(2)
            print(".")
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()