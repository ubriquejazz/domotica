#include "common.ino"

#define TIME_UP     30000   // tiempo que tarda la persiana en subir
#define TIME_DOWN   30000   // tiempo que tarda la persiana en bajar
#define RLAY1       13      // Lo conectamos a D7
#define RLAY2       12      // Lo conectamos a D6

// **** Globals **** //
int position_desired;     // actualizado por callback
int position_real;        // actualizado por callback
byte temp_subir = 0;      // flag de subida
byte temp_bajar = 0;      // flag de bajada
byte temp_bajar_p = 1;    // flag de parada
byte temp_subir_p = 1;    // flag de parada

void temp_parada(int value) {
  temp_subir_p = value;
  temp_bajar_p = value;
}

void subscribe_topics() {
  client.subscribe(MQTT_TOPIC "/comando");
  client.subscribe(MQTT_TOPIC "/set_position");
  client.subscribe(MQTT_TOPIC "/position");
}

void helper_setup() {
  pinMode(RLAY1, OUTPUT);
  digitalWrite(RLAY1, HIGH);
  pinMode(RLAY2, OUTPUT);
  digitalWrite(RLAY2, HIGH);
}

void helper_loop() {
  static int pos_str;
  static unsigned long previousMillis;
  unsigned long currentMillis, ahora;

  static unsigned long timeDown, timeUp;
  static unsigned long tiempoAnterior3 = 0;
  static unsigned long tiempoAnterior4 = 0;

  // Prepara contadores para inicializar temporizacion
  if (temp_subir_p == 1 && (position_desired > position_real)) {
    pos_str = position_desired;
    timeUp = (pos_str - position_real) * TIME_UP / 100;
    tiempoAnterior4 = millis();
    subiendo();
    temp_bajar = 0;
    temp_subir = 1;
  } 
  else if (temp_bajar_p == 1 && (position_real > position_desired)) {
    pos_str = position_desired;
    timeDown = (position_real - pos_str) * TIME_DOWN / 100;
    tiempoAnterior3 = millis();
    bajando();
    temp_bajar = 1;
    temp_subir = 0;
  }

  // Contadores para subir --> timeDown, tiempoAnterior3
  if (temp_subir == 1) {
    currentMillis = millis();
    if (currentMillis - previousMillis > 200UL) {
      position_real = (pos_str - (timeDown + tiempoAnterior3 - currentMillis) * 100 / TIME_UP);
      publish_position(position_real);
      previousMillis = currentMillis;
    }
    if (currentMillis - tiempoAnterior3 > timeDown) {
      position_desired = position_real;
      parada();
    }
  }

  // Contadores para bajar --> timeUp, tiempoAnterior4
  if (temp_bajar == 1) {
    currentMillis = millis();
    if (currentMillis - previousMillis > 200UL) {
      position_real = (pos_str + ((timeUp + tiempoAnterior4 - currentMillis) * 100 / TIME_DOWN));
      publish_position(position_real);
      previousMillis = currentMillis;
    }
    if (currentMillis - tiempoAnterior4 > timeUp) {
      position_desired = position_real;
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
    // Recibimos set_position
    position_desired = atof(payloadStr.c_str());
    temp_parada(1);
  } else if (strcmp(topic, MQTT_TOPIC "/comando") == 0) {
    // Recibimos comando de la Raspberry
    if (payloadStr == "subiendo") {
      position_desired = 100;
    } else if (payloadStr == "bajando") {
      position_desired = 0;
    } else if (payloadStr == "parada") {
      position_desired = position_real;
      parada();
    }
  }
}

void parada() {
  digitalWrite(RLAY2, HIGH);
  digitalWrite(RLAY1, HIGH);
  Serial.println("PARADA");
  client.publish(MQTT_TOPIC "/estado", "parada");
  client.publish(MQTT_TOPIC "/position", 
    String(position_real).c_str(), true);
  temp_bajar = 0;
  temp_subir = 0;
  temp_parada(1);
}

void subiendo() {
  digitalWrite(RLAY1, LOW);
  digitalWrite(RLAY2, HIGH);
  Serial.println("SUBIENDO");
  client.publish(MQTT_TOPIC "/estado", "subiendo");
  temp_parada(0);
}

void bajando() {
  digitalWrite(RLAY1, HIGH);
  digitalWrite(RLAY2, LOW);
  Serial.println("BAJANDO");
  client.publish(MQTT_TOPIC "/estado", "bajando");
  temp_parada(0);
}