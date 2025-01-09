#import hcsr04
#from hcsr04 import HCSR04
#sensor = HCSR04(trigger_pin=13, echo_pin=15)

# Servo (ultrasound scan)
servo_right = 1
servo_centre = 120
servo_left = 240
servo_delay = 250 #ms
servo = machine.PWM(machine.Pin(25), freq=50)

def forward_distance () :
  servo.duty(servo_centre) #centre
  return 0
  return sensor.distance_cm()

def right_distance () :
  servo.duty(servo_right)
  sleep_ms(servo_delay)
  return 0
  return sensor.distance_cm()

def left_distance () :
  servo.duty(servo_left)
  sleep_ms(servo_delay)
  return 0
  return sensor.distance_cm()