AstroPi Code

Provides access to the AstroPi's buttons which aren't covered by the Sensehat software. Most sources use pygame to read the buttons, but I consider that ap[proach bloated, and completely unreasonable for a embedded device.

And so I've used Adafruit Blinka, digitalio, and debouncer to provide both polled and callback access to the buttons.

## Requirements: ##

https://github.com/adafruit/Adafruit_Blinka

Provide support for digitalio for reading the buttons

https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Debouncer/master/adafruit_debouncer.py

Provides debouncing for the buttons.

## Examples ##

Both ways of access use events that contains 3 fields:
1. _timestamp_: the result of `time.time()` when the event was detected
2. _button_: the relevant button, one of `'a'`, `'b'`, `'top'`, `'bottom'`, `'left'`, or `'right'`
3. _action_: what happened, one of `pressed` or `released`


### Polled access ###

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

1. The `AstroPi_Buttons` object must be regularly updated.
2. `get_events()` returns an array of press/release events (described above) detected on the most recent update.

### Callback access ###

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

1. Callback functions can take 0 or 1 argument, which is an event object as described above.
2. Updating is done automatically by the callback thread.
3. The thread is managed automatically as callbacks are added and removed.
