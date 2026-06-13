import RPi.GPIO as GPIO

class Rlay:
    def __init__(self, pin):
        """Initializes the relay pin on the Raspberry Pi Zero W."""
        self.pin = pin
        
        # Ensure we are using Broadcom (BCM) numbering
        # checked safely if another part of the script already called it
        try:
            GPIO.setmode(GPIO.BCM)
        except ValueError:
            pass 
            
        # Force the relay to start in the safe 'OFF' state on boot
        self.off()

    def on(self):
        """Triggers the Active-Low relay ON by dropping pin to 0V."""
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        """Turns the relay OFF by switching the pin to an INPUT circuit break."""
        GPIO.setup(self.pin, GPIO.IN)

    def status(self):
        """Returns 'ON' or 'OFF' based on the hardware state."""
        pin_function = GPIO.gpio_function(self.pin)
        pin_state = GPIO.input(self.pin)
        
        if pin_function == GPIO.OUT and pin_state == GPIO.LOW:
            return "ON"
        else:
            return "OFF"
