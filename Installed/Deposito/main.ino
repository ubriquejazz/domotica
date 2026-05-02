#include <Arduino.h>

// ---------- Pin definitions ----------
#define TRIG_PIN       5
#define ECHO_PIN       18
#define RS485_TX       17   // GPIO 17
#define RS485_RX       16   // GPIO 16
#define RS485_DE_RE    4    // tied together)
#define SENSOR_POWER   25   // MOSFET to enable sensor 

// ---------- Config ----------
#define SLEEP_TIME_SEC 300   // 5 minutes
#define SOUND_SPEED    0.0343 // cm/us

HardwareSerial RS485Serial(2);

// ---------- Function: measure distance ----------
float measureDistance() {
  // Ensure clean trigger
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(5);

  // Send pulse
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo
  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // timeout 30ms

  if (duration == 0) {
    return -1; // no reading
  }

  float distance = (duration * SOUND_SPEED) / 2.0;
  return distance;
}

// ---------- RS-485 send ----------
void rs485Send(String msg) {
  digitalWrite(RS485_DE_RE, HIGH); // transmit mode
  delay(2);

  RS485Serial.println(msg);

  RS485Serial.flush();
  delay(2);

  digitalWrite(RS485_DE_RE, LOW); // receive mode
}

// ---------- Setup ----------
void setup() {
  // GPIO setup
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RS485_DE_RE, OUTPUT);
  pinMode(SENSOR_POWER, OUTPUT);

  digitalWrite(RS485_DE_RE, LOW);
  digitalWrite(SENSOR_POWER, LOW);

  // Serial for RS-485
  RS485Serial.begin(9600, SERIAL_8N1, RS485_RX, RS485_TX);

  // Power ON sensor
  digitalWrite(SENSOR_POWER, HIGH);
  delay(500); // allow sensor to stabilize

  // Take multiple readings for stability
  float sum = 0;
  int valid = 0;

  for (int i = 0; i < 5; i++) {
    float d = measureDistance();
    if (d > 0) {
      sum += d;
      valid++;
    }
    delay(100);
  }
  float distance = (valid > 0) ? (sum / valid) : -1;

  // Prepare message
  String msg;
  if (distance > 0) {
    msg = "DIST:" + String(distance, 1) + "cm";
  } else {
    msg = "DIST:ERROR";
  }

  // Send via RS-485 and power OFF sensor
  rs485Send(msg);
  digitalWrite(SENSOR_POWER, LOW);

  // Go to deep sleep
  esp_sleep_enable_timer_wakeup((uint64_t)SLEEP_TIME_SEC * 1000000ULL);
  esp_deep_sleep_start();
}

// ---------- Loop ----------
void loop() {
  // never used
}