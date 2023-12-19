# L298N module



## 1 - Drive the motor

We will design a simple program to make the right wheel turn 0.5s in positive direction, stop 0.5s, turn 0.5s in negative direction and stop 0.5s. And the wheel will repeat the reaction.

```python
IN3 = Pin(13, machine.Pin.OUT)	# D9
IN4 = Pin(23, machine.Pin.OUT)	# D11
ENA = Pin(27, machine.Pin.OUT) 	# D6

IN1 = Pin(14, machine.Pin.OUT)	# D7
IN2 = Pin(12, machine.Pin.OUT)	# D12
ENB = Pin(16, machine.Pin.OUT)	# D5

def stop(t=0):
  	IN1.off(); IN2.off()
    IN3.off(); IN4.off()
    if t > 0 :
        sleep_ms(t)
def forward(t=0):
    IN1.off(); IN2.on()
    IN3.on(); IN4.off()
    if t > 0 :
        sleep_ms(t)
def back(t=0):
    IN1.on(); IN2.off()
    IN3.off(); IN4.on()
    if t > 0 :
        sleep_ms(t)
        
ENA.on()
ENB.on()
while True:
    forward(500)
    stop(500)
    back(500)
    stop(500)
```

## 2 - Move and Turn

| Wheel | Forward | Go Back | Stop |
| ----- | ------- | ------- | ---- |
| Left  | FWD     | BACK    | STOP |
| Right | FWD     | BACK    | STOP |

| Wheel | Turn Right | Turn Left | Stop |
| ----- | ---------- | --------- | ---- |
| Left  | BACK       | FWD       | STOP |
| Right | FWD        | BACK      | STOP |

## 3 - Write the program

It may be a difficult for you to write the whole program to make the car move automatically. So we separate the movements into different function, for example moving forward and turning left. And when we write the program in the final step, we can call the function.

```c
pinMode(ENA, OUTPUT); 
pinMode(pinA1, OUTPUT); 
pinMode(pinA2, OUTPUT);

void motorAOn() { 
  digitalWrite(ENA, HIGH); 
}
void motorAForward() { 
  digitalWrite(pinA1, HIGH); 
  digitalWrite(pinA2, LOW); 
}
void motorABackward() { 
	digitalWrite(pinA1, LOW); 
  digitalWrite(pinA2, HIGH); 
}
void motorACoast() { 
  digitalWrite(pinA1, LOW); 
  digitalWrite(pinA2, LOW); 
}
void motorABrake() {
	digitalWrite(pinA1, HIGH); 
  digitalWrite(pinA2, HIGH); 
}

//Define High Level Commands
void enableMotors() {
	motorAOn(); 
  motorBOn(); 
}
void forward(int time) {
	motorAForward(); 
  motorBForward(); 
  delay(time); 
}
void turnRight(int time) {
	motorBBackward(); 
  motorAForward(); 
  delay(time); 
}
void turnLeft(int time) {
	motorABackward(); 
  motorBForward(); 
  delay(time); 
}
void coast(int time) {
	motorACoast(); 
  motorBCoast(); 
  delay(time); 
}
void brake(int time) {
	motorABrake(); 
  motorBBrake(); 
  delay(time); 
}
```

