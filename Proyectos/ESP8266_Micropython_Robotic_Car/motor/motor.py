# L298 Module

import machine
from machine import Pin, PWM, ADC, time_pulse_us

import time
from time import sleep, sleep_us, sleep_ms

import network, socket
wifi = network.WLAN(network.STA_IF)

IN1 = Pin(14, machine.Pin.OUT)
IN2 = Pin(12, machine.Pin.OUT)
ENB = Pin(16, machine.Pin.OUT)

IN3 = Pin(13, machine.Pin.OUT)
IN4 = Pin(23, machine.Pin.OUT)
ENA = Pin(27, machine.Pin.OUT)
        
class Motor():
    def __init__(self, IN1, IN2, EN):
        self.I1 = Pin(IN1, machine.Pin.OUT)
        self.I2 = Pin(IN2, machine.Pin.OUT)
        self.EN = Pin(EN, machine.Pin.OUT)
        self.EN.on() 
    def forward(self):
        self.I1.off(); self.I2.on()    
    def back(self):
        self.I1.on(); self.I2.off()
    def stop(self):
        self.I1.off(); self.I2.off()
        
motorA = Motor(14, 12, 16)
motorB = Motor(23, 13, 27)

def forward(t=0):
    motorA.forward()
    motorB.forward()
    if t > 0 :
        sleep_ms(t)
def back(t=0):
    motorA.back()
    motorB.back()
    if t > 0 :
        sleep_ms(t) 
def turnLeft(t=0):
    motorA.back()
    motorB.forward()
    if t > 0 :
        sleep_ms(t)
def turnRight(t=0):
    motorA.forward()
    motorB.back()
    if t > 0 :
        sleep_ms(t)
def stop(t=0):
    motorA.stop()
    motorB.stop()
    if t > 0 :
        sleep_ms(t)
        
# main
wifi.active(True)
wifi.connect('WIFI PEPI', '123456PEPI789')

if wifi.isconnected() :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 6666))
    print('UDP server config:', wifi.ifconfig(), 'on port 6666')
    while True:
        data, address = s.recvfrom(256)
        if data == b'0':
            stop(500)
            print("stop")
        elif data == b'q':
            forward(500)
            print("go")
        elif data == b'a':
            back(500)
            print("back")
        elif data == b'o':
            turnLeft(500)
            print("left")
        elif data == b'p':
            turnRight(500)
            print("right")
        else:
            print("error")
else  :
    print('No Wifi')        
    

