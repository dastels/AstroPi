from sense_hat import SenseHat
from time import sleep
from astropi_buttons import AstroPi_Buttons

sense = SenseHat()
buttons = AstroPi_Buttons()

e = (0, 0, 0)
w = (255, 255, 255)
sense.set_rotation(270)
sense.clear()
while True:
    buttons.update()
    for event in buttons.get_events():
        if event.action == "pressed":
            # Check which direction
            if event.button == "a":
                sense.show_letter("A")      # Up arrow
            elif event.button == "b":
                sense.show_letter("B")      # Down arrow
            elif event.button == "top":
                sense.show_letter("U")      # Up arrow
            elif event.button == "bottom":
                sense.show_letter("D")      # Down arrow
            elif event.button == "left":
                sense.show_letter("L")      # Left arrow
            elif event.button == "right":
                sense.show_letter("R")      # Right arrow
        # Wait a while and then clear the screen
        sleep(0.5)
        sense.clear()
