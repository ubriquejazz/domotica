
Integrating GitHub Actions with actual hardware requires a strategy to connect your hardware test environment to the CI/CD pipeline. Here's a step-by-step guide to achieve this:


## The basic idea

Your hardware is connected to a host machine (e.g., a Raspberry Pi, a dedicated PC, or a server) that can run commands and communicate with GitHub Actions.
Use a self-hosted runner installed on the host machine to execute tests directly on the hardware.

### Setup the Self-Hosted Runner

Step 1: Prepare the Host Machine

- Ensure the host machine has access to the hardware (e.g., through serial ports, GPIO, or network).

- Install necessary dependencies to run the tests (e.g., Python, firmware tools, Docker).

Step 2: Install the Runner

- Go to your GitHub repository:
    Navigate to Settings > Actions > Runners.
    Click Add Runner and follow the instructions to download and set up the runner.
- Run the commands provided to register and start the runner.

Step 3: Configure the Runner as a Service

- Set up the runner as a service to ensure it starts automatically on reboot:

    ./svc.sh install
    ./svc.sh start

###  Update the GitHub Actions Workflow

Use the self-hosted runner to execute tests on the hardware.

    hw_test.yaml

###  Hardware Communication in Tests

In your Python script (e.g., hardware_test.py):

Serial Communication: Use libraries like pyserial to communicate with devices via UART or USB.

    import serial

    # Connect to the hardware
    ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

    # Send and receive data
    ser.write(b'TEST_COMMAND\n')
    response = ser.readline()
    print(f"Response: {response}")

GPIO Control: For devices like Raspberry Pi, use libraries like RPi.GPIO or gpiozero.

        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)

        # Blink an LED
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)

Networking: For devices accessible over the network, use protocols like SSH (paramiko) or HTTP (requests).

### Test Artifacts and Logs

Collect logs or test artifacts from the hardware for review:

    Save logs to a file (e.g., hardware_logs.txt).
    Upload the file as an artifact in the workflow:

    - name: Upload logs
      uses: actions/upload-artifact@v3
      with:
        name: hardware-logs
        path: hardware_logs.txt


## Example 

Here’s an example setup for testing a device over a serial connection where sending the command ? should return OK.

### Python Test Script

The script sends the ? command over a serial connection and verifies that the response is OK.

    hardware_test.py

### GitHub Actions Workflow

The workflow uses a self-hosted runner that has access to the hardware.

    .github/workflows/hardware_test.yml

### Steps to Execute Locally

- Connect Hardware: Ensure the device is connected to the correct serial port (e.g., /dev/ttyUSB0 or COM3).

- Verify the connection using a serial terminal (e.g., minicom or PuTTY).

- Run the Test:

    python hardware_test.py

Expected Output:

If the test passes:

    Test passed: Received 'OK'

If the test fails:

    Test failed: Expected 'OK', but got 'ERROR'

### Debugging Tips

- Check Serial Port: Ensure the correct port (/dev/ttyUSB0, COM3, etc.) is specified in the script.
- Baudrate: Verify the device’s baud rate matches the script (e.g., 115200).
- Timeouts: If no response is received, try increasing the timeout in serial.Serial().
