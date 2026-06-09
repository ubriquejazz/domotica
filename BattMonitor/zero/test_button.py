# each button to a GPIO pin and the other side to a Ground (GND) pin. 
# This uses the Pi's internal pull-up resistors. Use python3-gpiozero!!

from gpiozero import Button
from signal import pause

# Define the buttons using their GPIO (BCM) numbers
btn1 = Button(17)
btn2 = Button(27)
btn3 = Button(22)
btn4 = Button(23)

# Define what happens when a button is pressed
def button_1_pressed():
    print("Button 1 (GPIO 17) pressed!")

def button_2_pressed():
    print("Button 2 (GPIO 27) pressed!")

def button_3_pressed():
    print("Button 3 (GPIO 22) pressed!")

def button_4_pressed():
    print("Button 4 (GPIO 23) pressed!")

# Assign the functions to the 'when_pressed' event
btn1.when_pressed = button_1_pressed
btn2.when_pressed = button_2_pressed
btn3.when_pressed = button_3_pressed
btn4.when_pressed = button_4_pressed

print("System Ready. Press a button (Ctrl+C to exit)...")

# Keep the script running
pause()