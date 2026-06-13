from machine import UART, Pin
from lcd1602 import LCD
import utime

USE_LCD = 0
DBG_MODE = 1
DBG_SEC = 10 # seconds

def percentage(ciclos: int):
    # 1. Calcular distancia base
    distancia_cm = ciclos // 3  
    
    # 2. Caso: Tanque Lleno / Zona Muerta del sensor
    if distancia_cm < 20:
        print("D: LLENO | V: 6000L\r\n", end="")
        return

    # 3. Calcular altura limitando a un mínimo de 0 cm
    altura_agua_cm = max(0, 220 - distancia_cm)

    # 4. Calcular litros (31.4 litros por cm) y limitar a un máximo de 6000L
    litros_actuales = min(6000, (altura_agua_cm * 314) // 10)

    # 5. Imprimir resultado
    print(f"D: {distancia_cm}cm | H: {altura_agua_cm}cm | V: {litros_actuales}L\r\n", end="")
    
def process(buffer):
    try:
        # Decode bytes to a regular string and strip whitespace/newlines
        line_str = buffer.decode('utf-8').strip()
        if USE_LCD: lcd.write(0,1, line_str)
        print(line_str)
        #ciclos_input = int(line_str)               
        #percentage(ciclos_input)
        
    except ValueError:
        print(f"[ERROR] Datos corruptos recibidos en UART: {buffer}")
    except Exception as e:
        # Cualquier otro error inesperado va solo a la PC
        print(f"[ERROR] Crítico: {str(e)}")

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
led = Pin("LED", Pin.OUT)

if USE_LCD:
    lcd = LCD() # Pin 6 and 7
    lcd.write(0,0, "Cicles:")
else:
    print("Cicles:")

buffer = b"" # Byte buffer to accumulate incoming characters
cnt = 0
while True:
    if DBG_MODE:
        led.toggle()
        utime.sleep_ms(SEC * 1000)
        print(cnt)
        cnt += 1

    else:
        if uart.any():
            incoming_bytes = uart.read()
            buffer += incoming_bytes      
            if b'\n' in buffer:
                process(buffer)
                buffer = b""
        utime.sleep_ms(10)    