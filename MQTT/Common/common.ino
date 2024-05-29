//// https://www.youtube.com/@ArduBrico ////

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "config.h"

WiFiClient espClient;
PubSubClient client(espClient);

void mierda();

void setup_wifi() {
  delay(5);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);

  // Static IP
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    for (int i = 0; i <= 50; i++) {
      delay(10);
      if (i == 50) {
        Serial.println(".");
      } else {
        Serial.print(".");
      }
    }
  }
  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(9600);
  delay(10);
  pinMode(RLAY1, OUTPUT);
  digitalWrite(RLAY1, HIGH);
  pinMode(RLAY2, OUTPUT);
  digitalWrite(RLAY2, HIGH);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  // Reconnect
  if (WiFi.status() != WL_CONNECTED) {
    setup_wifi();
    reconnect();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
  }
  // Standard loop
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  mierda();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(CLIENT_ID, mqttusuario, mqttpass)) {
      Serial.println("connected");
      delay(20);
      client.subscribe(MQTT_TOPIC "/comando");
      client.subscribe(MQTT_TOPIC "/set_position");
      client.subscribe(MQTT_TOPIC "/position");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      for (int i = 0; i <= 500; i++) {
        delay(10);
        if (i == 50) {
          Serial.println(".");
        } else {
          Serial.print(".");
        }
      }
    }
  } // end while
}

void publish_position(int position) {
  char message[10];
  snprintf(message, 10, "%d", position);
  client.publish(MQTT_TOPIC "/position", message);
}
