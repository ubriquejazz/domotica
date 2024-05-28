//// https://www.youtube.com/@ArduBrico ////

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "config.h"

#define CLIENT_ID   "Persiana_Sala"   // ID único en tu sistema
#define MQTT_TOPIC  "persianas/sala"  // mismo que tengas en configuration.yaml
#define TIME_UP     30000   // tiempo que tarda la persiana en subir
#define TIME_DOWN   30000   // tiempo que tarda la persiana en bajar
#define RLAY1       13;     // Lo conectamos a D7
#define RLAY2       12;     // Lo conectamos a D6

WiFiClient espClient;
PubSubClient client(espClient);

// Global variables (static)
int pos_str, pos_real;
int position_str, position_real, position_set;
byte temp_subir = 0;
byte temp_bajar = 0;
byte temp_bajar_p = 1;
byte temp_subir_p = 1;
unsigned long tiempoAnterior = 0;
unsigned long tiempoAnterior2 = 0;
unsigned long tiempoAnterior3 = 0;
unsigned long tiempoAnterior4 = 0;
unsigned long periodo3, periodo4;
unsigned long currentMillis;
unsigned long start, start2;

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

  ///// ACTIVAR CONTADOR PORCENTAJE 
  if (temp_subir_p == 1 && (position_str > position_real)) {
    periodo3 = ((position_str - position_real) * TIME_UP / 100);
    pos_str = position_str;
    digitalWrite(RLAY1, LOW);
    digitalWrite(RLAY2, HIGH);
    Serial.println("SUBIENDO");
    tiempoAnterior3 = millis();
    client.publish(MQTT_TOPIC "/estado", "subiendo");
    temp_bajar = 0;
    temp_subir = 1;
    temp_subir_p = 0;
    temp_bajar_p = 0;
  } else if (temp_bajar_p == 1 && (position_real > position_str)) {
    periodo4 = ((position_real - position_str) * TIME_DOWN / 100);
    pos_real = position_real;
    pos_str = position_str;
    digitalWrite(RLAY1, HIGH);
    digitalWrite(RLAY2, LOW);
    Serial.println("BAJANDO");
    tiempoAnterior4 = millis();
    client.publish(MQTT_TOPIC "/estado", "bajando");
    temp_bajar = 1;
    temp_subir = 0;
    temp_subir_p = 0;
    temp_bajar_p = 0;
  }

  ///// CONTADOR SUBIR PORCENTAJE ////
  if (temp_subir == 1) {
    currentMillis = millis();
    if (currentMillis - start2 > 200UL) {
      int subiendo_str = (pos_str - (periodo3 + tiempoAnterior3 - currentMillis) * 100 / TIME_UP);
      char message[10];
      snprintf(message, 10, "%d", subiendo_str);
      position_real = subiendo_str;
      client.publish(MQTT_TOPIC "/position", message);
      start2 = currentMillis;
    }
    if (currentMillis - tiempoAnterior3 > periodo3) {
      parada();
    }
  }

  ///// CONTADOR BAJAR PORCENTAJE ////
  if (temp_bajar == 1) {
    currentMillis = millis();
    if (currentMillis - start2 > 200UL) {
      int bajando_str = (pos_str + ((periodo4 + tiempoAnterior4 - currentMillis) * 100 / TIME_DOWN));
      char message[10];
      snprintf(message, 10, "%d", bajando_str);
      position_real = bajando_str;
      client.publish(MQTT_TOPIC "/position", message);
      start2 = currentMillis;
    }
    if (currentMillis - tiempoAnterior4 > periodo4) {
      parada();
    }
  }
}


void callback(char* topic, byte* payload, unsigned int length) {
  String payloadStr = "";
  for (int i = 0; i < length; i++) {
    payloadStr += (char)payload[i];
  }
  if (strcmp(topic, MQTT_TOPIC "/set_position") == 0) {
    int position_set = atof(payloadStr.c_str());
    position_str = position_set;
    temp_subir_p == 1;
    temp_bajar_p == 1;
  } else if (strcmp(topic, MQTT_TOPIC "/position") == 0) {
    float position_pos = atof(payloadStr.c_str());
    position_real = position_pos;
    position_str = position_pos;
    int position_pos2 = position_pos;
    client.unsubscribe(MQTT_TOPIC "/position");
  } else if (strcmp(topic, MQTT_TOPIC "/comando") == 0) {

    String message = payloadStr;
    if (message == "subiendo") {
      position_str = 100;
    } else if (message == "bajando") {
      position_str = 0;
    } else if (message == "parada") {
      parada();
    }
  }
}

void parada() {
  digitalWrite(RLAY2, HIGH);
  digitalWrite(RLAY1, HIGH);
  position_str = position_real;
  Serial.println("PARADA");
  String position_ = String(position_real);
  client.publish(MQTT_TOPIC "/estado", "parada");
  client.publish(MQTT_TOPIC "/position", position_.c_str(), true);
  temp_bajar = 0;
  temp_subir = 0;
  temp_subir_p = 1;
  temp_bajar_p = 1;
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
