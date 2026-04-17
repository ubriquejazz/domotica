#include <stdio.h>
 
#define trigPin 12
#define echoPin 11
 
long duration;
int distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}
 
void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  duration = pulseIn(echoPin, HIGH);
  distance = duration*0.034/2;
 
  Serial.print("Distance = ");
  Serial.print(distance);
  Serial.println(" cm");
}