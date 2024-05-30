/* Copia y pega el siguiente código en la configuración de mqtt dentro de tu Home Assitant:    
  
  sensor:  
    - name: "Sensor de lluvia"
      unique_id: "Sensor_lluvia"
      state_topic: "sensores/lluvia"        
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "../data/config.h"

#define SensorAnalog A0

WiFiClient espClient;
PubSubClient client(espClient);

int valor = 450; // Valor que queremos que sea el limite para detectar la lluvia
int estado = 0;
int llueve = 0;
int no_llueve = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Iniciando");
  delay(10);
  setup_wifi(); 
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
   setup_wifi();
   reconnect();
   client.setServer(mqtt_server, 1883);
  } 
  if (!client.connected()) {
   reconnect();
  }
  
  int SensorAnalogVal = analogRead(SensorAnalog); 
  if ((SensorAnalogVal<valor)){
   estado = 1;
   delay(100);     
  }
  if ((SensorAnalogVal>valor)){
   estado = 0;
   delay(100);     
  }
  if ((estado==1)&&(llueve==0)){
    Serial.println("Llueve");
    Serial.println (SensorAnalogVal);
    client.publish(MQTT_TOPIC"", "Llueve", true);
    llueve = 1;
    no_llueve = 0;
    delay(100);
  }
  if ((estado==0)&&(no_llueve==0)){
    Serial.println("No llueve");
    Serial.println (SensorAnalogVal);
    client.publish(MQTT_TOPIC"", "No llueve", true);
    no_llueve = 1;
    llueve = 0;
    delay(100);
  }
  client.loop();
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Conectando a  ");
  Serial.println(ssid); 
  WiFi.mode(WIFI_STA); //ESP in connect to network mode
  WiFi.begin(ssid, password); 

  while (WiFi.status() != WL_CONNECTED) {
    // wait 50 * 10 ms = 500 ms to give ESP some time to connect (need to give delay else you get soft WDT reset)
      for (int i=0; i <= 50; i++){
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

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Intentando conectar con MQTT...");
    // Attempt to connect
    if (client.connect(CLIENT_ID, mqttusuario, mqttpass)) {
      Serial.println("Conectado");
    } else {
      Serial.print("fallo, rc=");
      Serial.print(client.state());
      Serial.println(" volver a conectar en 5 segundos");

      // Wait (500 * 10ms = 5000ms) 5 seconds before retrying, but read button press meanwhile
      for (int i=0; i <= 500; i++){
        delay(10);
        if (i == 50) { 
          Serial.println(".");
        } else {
          Serial.print(".");
        }     
      }     
    }
  }
}
