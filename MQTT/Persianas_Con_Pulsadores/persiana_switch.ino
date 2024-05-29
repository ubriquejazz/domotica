#include "common.ino"

#define CLIENT_ID "Persiana_Sala"          // debe ser único en tu sistema
#define MQTT_TOPIC "persianas/sala"        // debe que ser el mismo que tengas en configuration.yaml

#define RLAY1       13    // Lo conectamos a D7
#define RLAY2       12    // Lo conectamos a D6
#define SW_UP       5     // Pulsador subir lo conectamos a  D1
#define SW_DOWN     4     // Pulsador bajar lo conectamos a  D2

#define TIME_UP     15000   // tiempo que tarda la persiana en subir
#define TIME_DOWN   15000   // tiempo que tarda la persiana en bajar
#define RECONECT    20      // Segundos hasta nuevo intento de conexión

///// FIN DE PARAMETROS CONFIGURABLES /////

unsigned long periodo3;
unsigned long periodo4;
byte temp_subir = 0;
byte temp_bajar = 0;
byte temp_bajar_p = 1;
byte temp_subir_p = 1;
unsigned long tiempoAnterior = 0;
unsigned long tiempoAnterior2, start, start2;
unsigned long tiempoAnterior3 = 0;
unsigned long tiempoAnterior4 = 0;
unsigned long currentMillis;
int position_set;
int position_real;
int position_str;
int position_send;
int pos_str;
int pos_real;
int val1 = 0;
int val2 = 0;
int old_val1 = 0;
int old_val2 = 0;
int state = 0;
int old_state = 0;
int state2 = 0;
int old_state2 = 0;
unsigned long tiempo1;
unsigned long tiempo2;
unsigned long tiempomax1 = 100;
unsigned long tiempomax2 = 100;
bool flanco1 = false;
bool flanco2 = false;
bool flancowifi = true;
bool flancomqtt = false;
bool contador = false;
int cont = 0;
bool subiendo;
bool bajando;

WiFiClient espClient;
PubSubClient client(espClient);

const char* topic = MQTT_TOPIC "/comando";
const char* topic_set = MQTT_TOPIC "/set_position";
const char* topic_pos = MQTT_TOPIC "/position";

void helper_setup() {
  digitalWrite(RLAY1, HIGH);  // Cambiar a LOW si funciona a la inversa
  digitalWrite(RLAY2, HIGH);  // Cambiar a LOW si funciona a la inversa
  pinMode(RLAY1, OUTPUT);
  pinMode(RLAY2, OUTPUT);
  pinMode(SW_UP, INPUT_PULLUP);   // Utilizamos la resistencia interna de la placa
  pinMode(SW_DOWN, INPUT_PULLUP); // Utilizamos la resistencia interna de la placa
}

void helper_loop() {
  

  ///// INTENTAMOS CONECTAR A WIFI, SI NO CONECTA, ESPERAMOS UN TIEMPO /////

  if ((WiFi.status() != WL_CONNECTED) && (flancowifi == true)) {
    setup_wifi();
    reconnect();
    client.setServer(mqtt_server, mqttport);
    client.setCallback(callback);
  }
  if (!client.connected()) {
    contador = true;
    cont++;
    delay(10);
  }

  if ((contador == true) && (cont == RECONECT * 100)) {
    flancomqtt = true;
    flancowifi = true;
    reconnect();
  }
  client.loop();


  ///// PULSADOR SUBIR ////

  val1 = digitalRead(SW_UP);

  if (!val1 && old_val1) {
    tiempo1 = millis();
    flanco1 = true;
  }
  old_val1 = val1;

  if (flanco1 && !val1)
    if (millis() - tiempo1 >= tiempomax1) {
      state = 1 - state;
      flanco1 = false;
    } else
      state2 = state2;
  else {
    flanco1 = false;
  }

  ///// PULSADOR BAJAR ////

  val2 = digitalRead(SW_DOWN);

  if (!val2 && old_val2) {
    tiempo2 = millis();
    flanco2 = true;
  }
  old_val2 = val2;

  if (flanco2 && !val2)
    if (millis() - tiempo2 >= tiempomax2) {
      state2 = 1 - state2;
      flanco2 = false;
    } else
      state2 = state2;
  else {
    flanco2 = false;
  }

  ///// ACCION PULSADORES /////

  if (state == 1 && old_state == 0 && bajando == true) {
    parada();

  } else if (state == 1 && old_state == 0 && bajando == false) {
    position_str = 100;
    subiendo = true;
    bajando = false;

  } else if (state == 0 && old_state == 1) {
    parada();
  }
  old_state = state;

  if (state2 == 1 && old_state2 == 0 && subiendo == true) {
    parada();

  } else if (state2 == 1 && old_state2 == 0 && subiendo == false) {
    position_str = 0;
    bajando = true;
    subiendo = false;

  } else if (state2 == 0 && old_state2 == 1) {
    parada();
  }

  old_state2 = state2;

  ///// ACTIVAR CONTADOR PORCENTAJE ////

  if (temp_subir_p == 1 && (position_str > position_real)) {
    periodo3 = ((position_str - position_real) * TIME_UP / 100);
    pos_str = position_str;
    digitalWrite(RLAY1, LOW);
    digitalWrite(RLAY2, HIGH);
    Serial.println("SUBIENDO");
    subiendo = true;
    bajando = false;
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
    subiendo = false;
    bajando = true;
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

void setup_wifi() {
  delay(10);
  // Nos conectamos a la Red
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while ((WiFi.status() != WL_CONNECTED) && (flancowifi == true)) {  // Intenamos conectar a Wifi durante 5 segundos
    for (int i = 0; i <= 5; i++) {
      Serial.println(i);
      delay(1000);
      if (i == 5) {
        flancowifi = false;
        contador = true;
        break;
      }
    }
  }
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("No se ha podido conectar al Wifi, nuevo intento en ");  // Intenamos conectar al Wifi durante los segundos configurados.
    Serial.print(RECONECT);
    Serial.println(" segundos...");
    flancowifi = false;
  } else {
    Serial.println("");
    Serial.println("WiFi conectado");
    Serial.println("Dirección IP: ");
    Serial.println(WiFi.localIP());
    cont = 0;
    flancowifi = false;
    contador = false;
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String payloadStr = "";
  for (int i = 0; i < length; i++) {
    payloadStr += (char)payload[i];
  }

  if (strcmp(topic, topic_set) == 0) {
    int position_set = atof(payloadStr.c_str());
    position_str = position_set;
    temp_subir_p == 1;
    temp_bajar_p == 1;
  } else if (strcmp(topic, topic_pos) == 0) {
    float position_pos = atof(payloadStr.c_str());
    position_real = position_pos;
    position_str = position_pos;
    int position_pos2 = position_pos;
    client.unsubscribe(topic_pos);
  } else if (strcmp(topic, topic) == 0) {

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
  Serial.print(position_);
  Serial.println(" %");
  temp_bajar = 0;
  temp_subir = 0;
  temp_subir_p = 1;
  temp_bajar_p = 1;
  state = 0;
  old_state = 0;
  state2 = 0;
  old_state2 = 0;
  subiendo = false;
  bajando = false;
}

void reconnect() {

  while ((!client.connected()) && (flancomqtt == true)) {
    Serial.println("Conectando con MQTT");
    if (client.connect(CLIENT_ID, mqttusuario, mqttpass)) {
      Serial.println("conectado");
      String position_ = String(position_real);
      client.publish(MQTT_TOPIC "/position", position_.c_str(), true);
      flancomqtt = false;
      delay(20);
      client.subscribe(MQTT_TOPIC "/comando");
      client.subscribe(MQTT_TOPIC "/set_position");
      client.subscribe(MQTT_TOPIC "/position");

    } else if (flancomqtt == true) {
      Serial.print("No se ha podido conectar, nuevo intento en ");  // Intenamos conectar al servidos MQTT durante los segundos configurados.
      Serial.print(RECONECT);
      Serial.println(" segundos...");
      cont = 0;
      flancowifi = false;
      flancomqtt = false;
      contador = true;
    }
  }
}
