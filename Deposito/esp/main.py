from machine import UART, Pin
from lcd1602 import LCD
import utime

def process_meas(ciclos: int):
    # 1. Calculate values using integer division (//)
    distancia_cm = ciclos // 3  
    altura_agua_cm = 220 - distancia_cm

    # 2. Case: Tank Full / Dead Zone
    if distancia_cm < 20:
        print("D: LLENO | V: 6000L\r\n", end="")
        return

    if altura_agua_cm < 0:
        altura_agua_cm = 0

    # 3. Calculate liters (31.4 liters per cm)
    litros_actuales = (altura_agua_cm * 314) // 10
    if litros_actuales > 6000:
        litros_actuales = 6000

    # 4. Print directly to the console
    print(f"D: {distancia_cm}cm | H: {altura_agua_cm}cm | V: {litros_actuales}L\r\n", end="")

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
lcd = LCD(); # 6 and 7
lcd.write(0,0, "Cicles:");
buffer = b"" # Byte buffer to accumulate incoming characters

while True:

    if uart.any():
        incoming_bytes = uart.read()
        buffer += incoming_bytes      
        if b'\n' in buffer:
            try:
                # Decode bytes to a regular string and strip whitespace/newlines
                line_str = buffer.decode('utf-8').strip()
                lcd.write(0,1, line_str);
                ciclos_input = int(line_str)               
                process_meas(ciclos_input)
                
            except ValueError:
                print(f"[ERROR] Datos corruptos recibidos en UART: {buffer}")
            except Exception as e:
                # Cualquier otro error inesperado va solo a la PC
                print(f"[ERROR] Crítico: {str(e)}")
                
            # Limpiamos el buffer para la siguiente lectura 
            buffer = b""
            
    # Small sleep to prevent core overheating, keeps polling highly responsive
    utime.sleep_ms(10)    