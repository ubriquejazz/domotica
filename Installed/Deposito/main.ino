char data[6];  // 5 bytes + null terminator

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() >= 5) {
    int bytesRead = Serial.readBytes(data, 5);
    data[bytesRead] = '\0';  // Null-terminate the string

    Serial.print("Received: ");
    Serial.println(data);
  }
}