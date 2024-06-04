#include "common.ino"

#define RLAY1       13    // Lo conectamos a D7
#define RLAY2       12    // Lo conectamos a D6
#define SW_UP       5     // Pulsador subir lo conectamos a  D1
#define SW_DOWN     4     // Pulsador bajar lo conectamos a  D2

#define TIME_UP     15000   // tiempo que tarda la persiana en subir
#define TIME_DOWN   15000   // tiempo que tarda la persiana en bajar
#define RECONECT    20      // Segundos hasta nuevo intento de conexión

byte temp_subir = 0;
byte temp_bajar = 0;
byte temp_bajar_p = 1;
byte temp_subir_p = 1;

unsigned long start2;
unsigned long tiempoAnterior3 = 0;
unsigned long tiempoAnterior4 = 0;
unsigned long periodo3, periodo4;
unsigned long tiempo1, tiempo2;
unsigned long currentMillis;

int position_real;    // actualizado por callback
int position_ideal;   // actualizado por callback
int pos_str;

int old_val1 = 0;
int old_val2 = 0;
int state = 0;
int old_state = 0;
int state2 = 0;
int old_state2 = 0;

bool flanco1 = false;
bool flanco2 = false;
bool subiendo;
bool bajando;

void helper_setup() {
  digitalWrite(RLAY1, HIGH);  // Cambiar a LOW si funciona a la inversa
  digitalWrite(RLAY2, HIGH);  // Cambiar a LOW si funciona a la inversa
  pinMode(RLAY1, OUTPUT);
  pinMode(RLAY2, OUTPUT);
  pinMode(SW_UP, INPUT_PULLUP);   
  pinMode(SW_DOWN, INPUT_PULLUP);
}

void helper_loop() {
  // boton subir
  int val1 = digitalRead(SW_UP);
  if (!val1 && old_val1) {
    tiempo1 = millis();
    flanco1 = true;
  }
  old_val1 = val1;

  if (flanco1 && !val1)
    if (millis() - tiempo1 >= 100) {
      state = 1 - state;
      flanco1 = false;
    } else
      state2 = state2;
  else {
    flanco1 = false;
  }

  // boton bajar
  int val2 = digitalRead(SW_DOWN);
  if (!val2 && old_val2) {
    tiempo2 = millis();
    flanco2 = true;
  }
  old_val2 = val2;

  if (flanco2 && !val2)
    if (millis() - tiempo2 >= 100) {
      state2 = 1 - state2;
      flanco2 = false;
    } else
      state2 = state2;
  else {
    flanco2 = false;
  }

  // accion boton subir
  if (state == 1 && old_state == 0 && bajando == true) {
    parada();
  } else if (state == 1 && old_state == 0 && bajando == false) {
    position_ideal = 100;
    subiendo = true;
    bajando = false;
  } else if (state == 0 && old_state == 1) {
    parada();
  }
  old_state = state;

  // accion boton bajar
  if (state2 == 1 && old_state2 == 0 && subiendo == true) {
    parada();
  } else if (state2 == 1 && old_state2 == 0 && subiendo == false) {
    position_ideal = 0;
    bajando = true;
    subiendo = false;
  } else if (state2 == 0 && old_state2 == 1) {
    parada();
  }
  old_state2 = state2;

  // activar contador porcentaje
  if (temp_subir_p == 1 && (position_ideal > position_real)) {
    periodo3 = ((position_ideal - position_real) * TIME_UP / 100);
    pos_str = position_ideal;
    tiempoAnterior3 = millis();
    subiendo();
  } else if (temp_bajar_p == 1 && (position_real > position_ideal)) {
    periodo4 = ((position_real - position_ideal) * TIME_DOWN / 100);
    pos_str = position_ideal;
    tiempoAnterior4 = millis();
    bajando();
  }
  
  // contadores subir --> periodo3, tiempoAnterior3
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

  // contadores bajar --> periodo4, tiempoAnterior4
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
    int position_set = atof(payloadStr.c_str());
    position_ideal = position_set;
    temp_subir_p == 1;
    temp_bajar_p == 1;
  } else if (strcmp(topic, MQTT_TOPIC "/position") == 0) {
    float position_pos = atof(payloadStr.c_str());
    position_real = position_pos;
    position_ideal = position_pos;
    client.unsubscribe(MQTT_TOPIC "/position");
  } else if (strcmp(topic, MQTT_TOPIC "/comando") == 0) {
    String message = payloadStr;
    if (message == "subiendo") {
      position_ideal = 100;
    } else if (message == "bajando") {
      position_ideal = 0;
    } else if (message == "parada") {
      parada();
    }
  }
}

void parada() {
  digitalWrite(RLAY2, HIGH);
  digitalWrite(RLAY1, HIGH);
  Serial.println("PARADA");
  position_ideal = position_real;
  String position_ = String(position_real);
  client.publish(MQTT_TOPIC "/estado", "parada");
  client.publish(MQTT_TOPIC "/position", position_.c_str(), true);
  Serial.print(position_);
  Serial.println(" %");

  temp_bajar = 0;
  temp_subir = 0;
  temp_subir_p = 1;
  temp_bajar_p = 1;

  state = 0; old_state = 0;
  state2 = 0; old_state2 = 0;
  subiendo = false;
  bajando = false;
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
  subiendo = false;
  bajando = true;
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
  subiendo = true;
  bajando = false;
}