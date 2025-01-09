# ESP setup
- In Arduino IDE, go to Preferences->URL manager
- Install the module: ESP01 or ESP32
- Go to the library manager and install PubSubClient library
- Install de driver of the programmer (with the device already connected): http://sparks.gogo.co.nz/assets/_site_/downloads/CH340_WINDOWS.zip

### ESP01
- In Arduino IDE, go to Preferences->URL manager
- Fill the field with `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
- Install the library in the manager and choose "Generic ESP8266 module"

### ESP32
- Fill the field with `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
- Install the library in the manager and choose "ESP32 dev module"
