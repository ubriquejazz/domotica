# L298 Motor using PWM

IN1 = PWM(Pin(14))
IN2 = PWM(Pin(12))
IN3 = PWM(Pin(13))
IN4 = PWM(Pin(23))

minSpeed = 300
midSpeed = 700
maxSpeed = 1024
speed = midSpeed
action = 0

def setMotor(MotorPin, val):
  MotorPin.freq(50)
  MotorPin.duty(val)

def stop(t=0):
  setMotor(IN1, 0)
  setMotor(IN2, 0)
  setMotor(IN3, 0)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)

def forward(t=0):
  setMotor(IN1, speed)
  setMotor(IN2, 0)
  setMotor(IN3, speed)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)

def back(t=0):
  setMotor(IN1, 0)
  setMotor(IN2, speed)
  setMotor(IN3, 0)
  setMotor(IN4, speed)
  if t > 0 :
    sleep_ms(t)

def left (t=0):
  setMotor(IN1, 0)
  setMotor(IN2, speed)
  setMotor(IN3, speed)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)

def right (t=0):
  setMotor(IN1, speed)
  setMotor(IN2, 0)
  setMotor(IN3, 0)
  setMotor(IN4, speed)
  if t > 0 :
    sleep_ms(t)

def left_cruise (t=0):
  setMotor(IN1, 0)
  setMotor(IN2, 0)
  setMotor(IN3, speed)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)

def right_cruise (t=0):
  setMotor(IN1, speed)
  setMotor(IN2, 0)
  setMotor(IN3, 0)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)