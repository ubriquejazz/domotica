import RPi.GPIO as GPIO
import time

SW1 = 9
SW2 = 11

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def front_door(channel):
    print("Button was pushed!")
    time.sleep(0.1)

def back_door(channel):
    print("Button was pushed!")
    time.sleep(0.1)

GPIO.add_event_detect(SW1, GPIO.FALLING, callback=front_door)
GPIO.add_event_detect(SW2, GPIO.FALLING, callback=back_door)

try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
print("End of the program")