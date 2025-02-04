import serial
import time, sys

# Test parameters
COMMAND = "?"  # The command to send
EXPECTED = "OK"  # The expected response from the device

def test_serial_command(port, baudrate, command, expected_response):
    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for the connection to stabilize

        # Send the 'command followed by a newline character
        ser.write(f"{command}\n".encode("utf-8"))
        # ser.write(b'?\n')  
        response = ser.readline().decode('utf-8').strip()  # Read and decode response

        # Check the response
        if response != expected_response:
            raise AssertionError(f"Expected '{expected_response}', but got '{response}'")
        print("Test passed: Received 'OK'")

        # Close the connection
        ser.close()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Replace '/dev/ttyUSB0' with your device's serial port
    test_serial_command(port='/dev/ttyUSB0', baudrate=115200, COMMAND, EXPECTED)
