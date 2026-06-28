from machine import UART, Pin
from lcd1602 import LCD
import time

uart = UART(0, baudrate=4800, tx=Pin(0), rx=Pin(1))

# RS485 module
de = Pin(16, Pin.OUT)
de.off() # active-HIGH

re = Pin(17, Pin.OUT)
re.off() # active-LOW

if (False):
    lcd = LCD()
    lcd.write(0,0, "Jola")

while True:
    # Option 1: Send a single character using a byte string
    uart.write(b'H')
    print("Sent: H")
    
    # Tiny pause to let the hardware process the transmission
    time.sleep(0.05)
    
    if uart.any():
        data = uart.read(1) # Read 1 byte
        print(f"Received: {data.decode('utf-8')}")
    else:
        print("Received: Nothing (Check your jumper wire!)")
    print("--------------------------------------------")

    time.sleep(2)
