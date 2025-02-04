#include <DHT.h>

#define BTTN01   6
#define BTTN02   7
#define BTTN03   8
#define BTTN04   9
#define DELAY    5000

#define RLAY01   12
#define RLAY02   11
#define RLAY03   10
#define RLAY04    9

#define LED_PIN   LED_BUILTIN
#define DHTPIN    2       // Pin digital al que está conectado el sensor DHT
#define DHTTYPE   DHT11   // Cambia a DHT22 si usas ese modelo

// Variables globales
DHT dht(DHTPIN, DHTTYPE);
String command = "";
int ledState = HIGH;

void setup() {
  Serial.begin(9600); // Comunicación serial
  dht.begin();        // Inicializa el sensor
  pinMode(LED_PIN, OUTPUT);
  pinMode(RLAY01, OUTPUT);
  pinMode(RLAY02, OUTPUT);
  pinMode(BTTN01, INPUT);
  pinMode(BTTN02, INPUT);
  releOFF(0);

  Serial.println("Interprete de comandos listo. Escribe 'HELP' para ver los comandos disponibles.");
}

// Función para manejar los comandos
void handleCommand(String command) {
  if (command.equalsIgnoreCase("HELP")) {
    Serial.println("Comandos disponibles:");
    Serial.println("  LEDON - Enciende el LED interno.");
    Serial.println("  LEDOFF - Apaga el LED interno.");
    Serial.println("  STATUS - Muestra el estado del LED.");
    Serial.println("  GET_TEMP - Obtiene la temperatura actual.");
  } else if (command.equalsIgnoreCase("LEDON")) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("LED encendido.");
  } else if (command.equalsIgnoreCase("LEDOFF")) {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("LED apagado.");
  } else if (command.equalsIgnoreCase("STATUS")) {
    if (digitalRead(LED_BUILTIN) == HIGH) {
      Serial.println("LED está encendido.");
    } else {
      Serial.println("LED está apagado.");
    }
  } else if (command.equalsIgnoreCase("GET_TEMP")) {
    float temp = dht.readTemperature(); // Lee la temperatura en grados Celsius
    if (isnan(temp)) {
      Serial.println("Error al leer la temperatura.");
    } else {
      Serial.print("Temperatura actual: ");
      Serial.print(temp);
      Serial.println(" °C");
    }
  } else {
    Serial.println("Comando no reconocido. Escribe 'HELP' para ver los comandos disponibles.");
  }
}

void releOFF(int id) {
  if (id == 1) 
    digitalWrite(RLAY01, HIGH);
  else if (id == 2)
    digitalWrite(RLAY02, HIGH);
  else {
    digitalWrite(RLAY01, HIGH);
    digitalWrite(RLAY02, HIGH);  
  }
}

void releON(int id) {
  if (id == 1) 
    digitalWrite(RLAY01, LOW);
  else if (id == 2)
    digitalWrite(RLAY02, LOW);
}

void loopIzda() {
  static bool upRunning = false;
  static bool downRunning = false;

  static unsigned long startTimeUp = 0;
  static unsigned long elapsedTimeUp = 0;
  static unsigned long startTimeDwn = 0;
  static unsigned long elapsedTimeDwn = 0;

  if (!upRunning && !downRunning) { // solo en reposo cambio
    if (digitalRead(BTTN01) == LOW && digitalRead(BTTN02) == HIGH) {
      upRunning = true;
      startTimeUp = millis();
      releON(2);
    }
    else if (digitalRead(BTTN02) == LOW && digitalRead(BTTN01) == HIGH) {
      downRunning = true;
      startTimeDwn = millis();
      releON(1);
    }
  }
  
  if (upRunning && !downRunning) {
    elapsedTimeUp = millis() - startTimeUp;
    if (elapsedTimeUp > DELAY) {
      upRunning = false;
      releOFF(2);
    }
  }
  
 if (downRunning && !upRunning) {
    elapsedTimeDwn = millis() - startTimeDwn;
    if (elapsedTimeDwn > DELAY) {
      downRunning = false;
      releOFF(1);
    }
  }
}

void loopDcha() {
  static bool upRunning = false;
  static bool downRunning = false;

  static unsigned long startTimeUp = 0;
  static unsigned long elapsedTimeUp = 0;
  static unsigned long startTimeDwn = 0;
  static unsigned long elapsedTimeDwn = 0;
}

void loop() {
  loopIzda();
  //loopDcha();

  // Verifica si hay datos disponibles en el puerto serie
  if (Serial.available()) {
    command = Serial.readStringUntil('\n'); // Lee el comando hasta un salto de línea
    command.trim();                         // Elimina espacios y caracteres extra
    handleCommand(command);                 // Procesa el comando
  }
}