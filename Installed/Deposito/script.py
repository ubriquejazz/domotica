from machine import UART, Pin
import time

# Define UART pins
TX_PIN = 0
RX_PIN = 1

# Initialize UART for Modbus communication
uart = UART(0, baudrate=9600, tx=Pin(TX_PIN), rx=Pin(RX_PIN))

# Register Addresses
REG_CALC_DIST = 0x0100  # Calculated distance (500ms response)
REG_TEMP = 0x0102       # Temperature (100ms response)

def calculate_crc(frame):
    crc = 0xFFFF
    for pos in frame:
        crc ^= pos
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

def construct_modbus_request(start_high, start_low, count_high, count_low):
    frame = [0x01, 0x03, start_high, start_low, count_high, count_low]
    crc = calculate_crc(frame)
    frame.append(crc & 0xFF)         # CRC low byte
    frame.append((crc >> 8) & 0xFF)  # CRC high byte
    return bytes(frame)

def send_modbus_request(frame):
    uart.write(frame)

def read_modbus_response(length):
    response = uart.read(length)
    return response

def verify_crc(frame):
    if not frame or len(frame) < 3:
        return False
    received_crc = (frame[-1] << 8) | frame[-2]
    calculated_crc = calculate_crc(frame[:-2])
    return received_crc == calculated_crc


def get_sensor_data():
    # Frame: [01 03 01 00 00 01 85 F6]
    dist_req = construct_modbus_request(0x01, 0x00, 0x00, 0x01)
    send_modbus_request(dist_req)
    time.sleep_ms(600) # Response time is about 500ms 
    
    if uart.any():
        resp = uart.read()
        if resp and verify_crc(resp) and len(resp) >= 7:
            # Data is in bytes 3 and 4 [cite: 36, 45]
            dist_mm = (resp[3] << 8) | resp[4]
            print(f"Distance: {dist_mm} mm")
    
def get_sensor_temperature():
    
    # Frame: [01 03 01 02 00 01 24 36]
    temp_req = construct_modbus_request(0x01, 0x02, 0x00, 0x01)
    send_modbus_request(temp_req)
    
    time.sleep_ms(150) # Response time is about 100ms 
    
    if uart.any():
        resp = uart.read()
        if resp and verify_crc(resp) and len(resp) >= 7:
            raw_temp = (resp[3] << 8) | resp[4]
            # Convert UINT16 to signed INT16 if necessary
            if raw_temp > 32767:
                raw_temp -= 65536
            print(f"Temperature: {raw_temp / 10.0} °C")

def main():
    print("Starting Modbus Ultrasonic Sensor Reading...")
    while True:
        # Clear any old data sitting in the buffer
        if uart.any():
            uart.read()
            
        get_sensor_data()
        time.sleep_ms(100) # Small gap between requests
        get_sensor_temperature()
        print("-" * 20)
        time.sleep(2)

if __name__ == "__main__":
    main()