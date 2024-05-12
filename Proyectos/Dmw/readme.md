# Digital Manufacturing Week

The iFM has set up a ‘DMW factory’ production line which first featured at Digital Manufacturing Week in Liverpool, 10 & 11 November 2021 

## Common Hardware

- RPi4 connector mini-HDMI to HDMI
- Touchscreen cable DVI to HDMI
- Brazo con soporte para mesa y riel DIN para RPi4

### Job Tracking

- Scanner = ESP32-Cam + Battery
- Impresora de etiquetas portatil (BLE)

## Software

- Web server with javascript client subscribed to these stages/topic
    1. NewJob
    2. Assembling
    3. Packaging
    4. Completed

- Scanner with MQTT clients to publish -t "home/newJob" -m "11022033044"

