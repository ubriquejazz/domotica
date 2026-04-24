#include <SoftwareSerial.h>

// Sensor TX -> Nano D10, Sensor RX -> Nano D11
SoftwareSerial sensorSerial(10, 11);

void setup() {
  Serial.begin(9600);
  sensorSerial.begin(9600);
  Serial.println("Send 'M' to trigger a measurement...");
}

void loop() {
  // Check if you typed 'M' in the Serial Monitor
  if (Serial.available() > 0) {
    char incoming = Serial.read();
    if (incoming == 'M' || incoming == 'm') {
      Serial.println("Triggering sensor...");
      sensorSerial.write(0x55); // Send the trigger command
    }
  }

  // Check for the response from the sensor
  int dist = getDistance();
  if (dist > 0) {
    Serial.print("Distance: ");
    Serial.print(dist);
    Serial.println(" mm");
  }
}

int getDistance() {
  // We need at least 4 bytes in the buffer (0xFF, High, Low, Checksum)
  if (sensorSerial.available() >= 4) {
    if (sensorSerial.read() == 0xFF) {
      byte data[3];
      sensorSerial.readBytes(data, 3);

      byte highByte = data[0];
      byte lowByte  = data[1];
      byte checksum = data[2];

      if (((0xFF + highByte + lowByte) & 0xFF) == checksum) {
        return (highByte << 8) + lowByte;
      }
    }
  }
  return -1;
}