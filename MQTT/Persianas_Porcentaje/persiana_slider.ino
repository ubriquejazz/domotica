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

unsigned long tiempoAnterior3 = 0;
unsigned long tiempoAnterior4 = 0;
unsigned long periodo3, periodo4;

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
  static unsigned long start2;

  // Inicializa contadores
  if (temp_subir_p == 1 && (position_desired > position_real)) {
    periodo3 = ((position_desired - position_real) * TIME_UP / 100);
    pos_str = position_desired;
    tiempoAnterior3 = millis();
    subiendo();
  } else if (temp_bajar_p == 1 && (position_real > position_desired)) {
    periodo4 = ((position_real - position_desired) * TIME_DOWN / 100);
    pos_str = position_desired;
    tiempoAnterior4 = millis();
    bajando();
  }

  // Contadores para bajar --> periodo3, tiempoAnterior3
  if (temp_subir == 1) {
    currentMillis = millis();
    if (currentMillis - start2 > 200UL) {
      position_real = (pos_str - (periodo3 + tiempoAnterior3 - currentMillis) * 100 / TIME_UP);
      publish_position(position_real);
      start2 = currentMillis;
    }
    if (currentMillis - tiempoAnterior3 > periodo3) {
      parada();
    }
  }

  // Contadores para bajar --> periodo4, tiempoAnterior4
  if (temp_bajar == 1) {
    currentMillis = millis();
    if (currentMillis - start2 > 200UL) {
      position_real = (pos_str + ((periodo4 + tiempoAnterior4 - currentMillis) * 100 / TIME_DOWN));
      publish_position(position_real);
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
    // Recibimos set_position
    int position_set = atof(payloadStr.c_str());
    position_desired = position_set;
    temp_subir_p == 1;
    temp_bajar_p == 1;
  } else if (strcmp(topic, MQTT_TOPIC "/position") == 0) {
    // Recibimos position
    float position_pos = atof(payloadStr.c_str());
    position_real = position_pos;
    position_desired = position_pos;
    client.unsubscribe(MQTT_TOPIC "/position");
  } else if (strcmp(topic, MQTT_TOPIC "/comando") == 0) {
    // Recibimos comando de la Raspberry
    String message = payloadStr;
    if (message == "subiendo") {
      position_desired = 100;
    } else if (message == "bajando") {
      position_desired = 0;
    } else if (message == "parada") {
      parada();
    }
  }
}

void parada() {
  digitalWrite(RLAY2, HIGH);
  digitalWrite(RLAY1, HIGH);
  position_desired = position_real;
  Serial.println("PARADA");
  String position_ = String(position_real);
  client.publish(MQTT_TOPIC "/estado", "parada");
  client.publish(MQTT_TOPIC "/position", position_.c_str(), true);
  temp_bajar = 0;
  temp_subir = 0;
  temp_subir_p = 1;
  temp_bajar_p = 1;
}

void subiendo() {
  digitalWrite(RLAY1, LOW);
  digitalWrite(RLAY2, HIGH);
  Serial.println("SUBIENDO");
  client.publish(MQTT_TOPIC "/estado", "subiendo");
  temp_bajar = 0;
  temp_subir = 1;
  temp_subir_p = 0;
  temp_bajar_p = 0;
}

void bajando() {
  digitalWrite(RLAY1, HIGH);
  digitalWrite(RLAY2, LOW);
  Serial.println("BAJANDO");
  client.publish(MQTT_TOPIC "/estado", "bajando");
  temp_bajar = 1;
  temp_subir = 0;
  temp_subir_p = 0;
  temp_bajar_p = 0;
}