# Quick automation demo 

Here’s a Python script for the demo:

    hw_test.py

## Communication under tests

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

## Jenkins server

Ensure your C code is in a version control system (e.g., GitHub). This server has all the development tools installed (compiler, debugger, flash). Once the application is running it's able to communicate throught the serial port (CDC-USB)

Login to Jenkins and install:

- Git Plugin (to clone repositories).
- Python Plugin or ensure Python is installed on the system.

## Create a Jenkins job

Add a Build Step > Execute Shell.
Use this script to set up the virtual environment and run the tests:

    #!/bin/bash
    make build
    make flash

    python3 -m venv ~/entorno       # Create a virtual environment
    source ~/entorno/bin/activate   # Activate the environment
    pip install -r requirements.txt  # Install dependencies 
    python hw_test.py  # Run tests in the tests/ directory

## Automate builds

Go to Build Triggers in the job configuration and enable options **Poll SCM**: Automatically pull changes from the repository.

## Test Artifacts and Logs

Collect logs or test artifacts from the last build.
