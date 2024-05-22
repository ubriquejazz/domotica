const char* ssid  = "SSID";                 // Nombre de nuestra red Wifi
const char* password = "CONTRASEÑA";        // Contraseña de nuestra ede Wifi
const char* mqtt_server = "192.168.1.98";   // I.P. de nuestro servidor MQTT (Home Assistant)
int mqttport = 1883;
const char* mqttusuario = "MQTT";       // Nombre de usuario MQTT en Home Assistant
const char* mqttpass = "XXX";           // Contraseña para el usuario de MQTT
#define CLIENT_ID   "Puerta_Garaje"     // Nombre que le queramos dar al dispositivo                 
#define MQTT_TOPIC  "garaje"            // Topic raíz
#define LUZ   "garaje/luces/comando"    // Topic para encender la luz del garaje si la tenemos domotizada
