#include <SoftwareSerial.h>

// Sensor TX (Echo) -> Nano D10
// Sensor RX (Trig) -> Nano D11 (Unused in Auto Mode)
SoftwareSerial sensorSerial(10, 11);

void setup() {
  Serial.begin(9600);
  sensorSerial.begin(9600);
  Serial.println("SR04M-2 sensor: Ready.");
}

void loop() {
  int distance = getDistance();

  if (distance > 0) {
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" mm");
  } else {
    // Optional: Handle errors or "out of range"
    // Serial.println("Waiting for valid data...");
  }

  delay(100); // Small delay to match the sensor's 10Hz output
}

/**
 * Returns distance in mm, or -1 if no valid data is available
 */
int getDistance() {
  if (sensorSerial.available() >= 4) {
    // Sync: Look for the header byte 0xFF
    if (sensorSerial.read() == 0xFF) {
      byte data[3]; // We need the next 3 bytes: High, Low, Checksum
      
      // Read the remaining bytes
      sensorSerial.readBytes(data, 3);

      byte highByte = data[0];
      byte lowByte  = data[1];
      byte checksum = data[2];

      // Verification: Checksum is the sum of first 3 bytes (Header + High + Low)
      if (((0xFF + highByte + lowByte) & 0xFF) == checksum) {
        return (highByte << 8) + lowByte;
      }
    }
  }
  return -1; // Return -1 if data was invalid or not ready
}