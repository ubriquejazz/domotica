# Author: cheungbx  2020/04/30
# ESP8266 Micropython WIFI remote control and Autodrive car
#
# Author: ubriquejazz 2021/12/22
# ESP32_Micropython_Robotic_Car
# -----------------------------------

import machine
from machine import Pin, PWM, ADC, time_pulse_us

import time
from time import sleep, sleep_us, sleep_ms

import remote
from remote import remoteControl

import motor
from motor import stop, forward, right, left, right_cruise, left_cruise

import servo
from servo import right_distance, front_distance, left_distance
auto=False

def autoDrive () :
  # check distance from obstacles in cm.
  fd = forward_distance()
  print('forward ', fd)
  # then take actions in milli seconds
  if fd < 10 :
     stop(100)
     back(200)
     print ("+Auto Stop back")
  elif fd < 25 :
      stop(100)
      ld=left_distance ()
      rd=right_distance ()
      print('L ',ld, ' R ', rd)

      if ld < 15 and rd < 15 :
        # backward
        back(800)
        left(300)
        print ("+Auto back left")

      elif ld > rd :
        # left
        back(100)
        right(300)
        print ("+Auto left")

      else : # ld <= rd
        # right
        back(100)
        left(300)
        print ("+Auto right")
  else  : # >= 25
    # forward
    forward (100)
    print ("+Auto forward")

# main program starts here
print (forward_distance())

stop()

while True:
    if auto :
        autoDrive()
    elif wifi.isconnected()  :
        remoteControl()
