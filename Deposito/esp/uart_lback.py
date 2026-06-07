from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# MAX3485
enable = Pin(18, Pin.OUT)
enable.off()

# RS485 module
de = Pin(16, Pin.OUT)
de.off() # active-HIGH

re = Pin(17, Pin.OUT)
re.off() # active-LOW

while True:
    # Option 1: Send a single character using a byte string
    enable.on()    
    
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

    enable.off()
    time.sleep(2)
