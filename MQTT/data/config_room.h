const char* ssid = "SSID";                  // Nombre de tu SSID
const char* password = "PASSWORD";          // Contraseña de tu SSID
const char* mqtt_server = "XXX.XXX.X.XX";   // IP de tu servidor MQTT
const char* mqttusuario = "MQTT";           // Usuario MQTT en Home Assistant
const char* mqttpass = "PASS_MQTT";         // Contraseña para el usuario MQTT 

#define CLIENT_ID   "Persiana_Habitacion"   // ID único en tu sistema
#define MQTT_TOPIC  "persianas/room"  // mismo que tengas en cover.yaml