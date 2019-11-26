from sense_hat import SenseHat
from time import sleep
from astropi_buttons import AstroPi_Buttons

sense = SenseHat()
buttons = AstroPi_Buttons()

def a(event):
    if event.action == 'pressed':
        sense.show_letter("A")
    else:
        sense.clear()

def b(event):
    if event.action == 'pressed':
        sense.show_letter("B")
    else:
        sense.clear()

def top(event):
    if event.action == 'pressed':
        sense.show_letter("U")
    else:
        sense.clear()

def bottom(event):
    if event.action == 'pressed':
        sense.show_letter("B")
    else:
        sense.clear()

def left(event):
    if event.action == 'pressed':
        sense.show_letter("L")
    else:
        sense.clear()

def right(event):
    if event.action == 'pressed':
        sense.show_letter("R")
    else:
        sense.clear()

buttons.callback_a = a
buttons.callback_b = b
buttons.callback_top = top
buttons.callback_bottom = bottom
buttons.callback_left = left
buttons.callback_right = right

e = (0, 0, 0)
w = (255, 255, 255)
sense.set_rotation(270)
sense.clear()
while True:
    pass
