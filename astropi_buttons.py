import time
import board
import digitalio
import debouncer
from functools import wraps
from collections import namedtuple
from threading import Thread, Event
import inspect


AstroPiButtonEvent = namedtuple('AstroPiButtonEvent', ('timestamp', 'button', 'action'))

# If you have the buttons wired differently, tweak these.
BUTTON_A_PIN = board.D21
BUTTON_B_PIN = board.D16
BUTTON_TOP_PIN = board.D26
BUTTON_BOTTOM_PIN = board.D13
BUTTON_LEFT_PIN = board.D20
BUTTON_RIGHT_PIN = board.D19

BUTTON_A = 'a'
BUTTON_B = 'b'
BUTTON_TOP = 'top'
BUTTON_BOTTOM = 'bottom'
BUTTON_LEFT = 'left'
BUTTON_RIGHT = 'right'

ACTION_PRESSED  = 'pressed'
ACTION_RELEASED = 'released'
ACTION_HELD     = 'held'

class AstroPi_Buttons(object):


    def _make_debouncer(self, pin):
        io = digitalio.DigitalInOut(pin)
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        return debouncer.Debouncer(io)


    def __init__(self):
        """Set up button debouncers and callback support."""
        self._button_a = self._make_debouncer(BUTTON_A_PIN)
        self._button_b = self._make_debouncer(BUTTON_B_PIN)
        self._button_top = self._make_debouncer(BUTTON_TOP_PIN)
        self._button_bottom = self._make_debouncer(BUTTON_BOTTOM_PIN)
        self._button_left = self._make_debouncer(BUTTON_LEFT_PIN)
        self._button_right = self._make_debouncer(BUTTON_RIGHT_PIN)
        self._callbacks = {}
        self._callback_thread = None
        self._callback_event = Event()


    def update(self):
        """Update all the button debouncers.
        Just needed to be called explicitly when polling for events."""
        self._button_a.update()
        self._button_b.update()
        self._button_top.update()
        self._button_bottom.update()
        self._button_left.update()
        self._button_right.update()


    def get_events(self, now=time.time()):
        """Get any press/release events that occurred since the most recent update.
        Only needed to be called explicitly when polling for events.
        :param now: the time to stamp each event with
        """
        events = []
        if self._button_a.fell:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_A, action=ACTION_PRESSED))
        if self._button_a.rose:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_A, action=ACTION_RELEASED))
        if self._button_b.fell:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_B, action=ACTION_PRESSED))
        if self._button_b.rose:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_B, action=ACTION_RELEASED))
        if self._button_top.fell:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_TOP, action=ACTION_PRESSED))
        if self._button_top.rose:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_TOP, action=ACTION_RELEASED))
        if self._button_bottom.fell:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_BOTTOM, action=ACTION_PRESSED))
        if self._button_bottom.rose:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_BOTTOM, action=ACTION_RELEASED))
        if self._button_left.fell:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_LEFT, action=ACTION_PRESSED))
        if self._button_left.rose:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_LEFT, action=ACTION_RELEASED))
        if self._button_right.fell:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_RIGHT, action=ACTION_PRESSED))
        if self._button_right.rose:
            events.append(AstroPiButtonEvent(timestamp=now, button=BUTTON_RIGHT, action=ACTION_RELEASED))
        return events


    def _wrap_callback(self, fn):
        # Shamelessley nicked (with some variation) from the AstroPi joystick code :)
        @wraps(fn)
        def wrapper(event):
            return fn()

        if fn is None:
            return None
        elif not callable(fn):
            raise ValueError('value must be None or a callable')
        elif inspect.isbuiltin(fn):
            # We can't introspect the prototype of builtins. In this case we
            # assume that the builtin has no (mandatory) parameters; this is
            # the most reasonable assumption on the basis that pre-existing
            # builtins have no knowledge of InputEvent, and the sole parameter
            # we would pass is an InputEvent
            return wrapper
        else:
            # Try binding ourselves to the argspec of the provided callable.
            # If this works, assume the function is capable of accepting no
            # parameters and that we have to wrap it to ignore the event
            # parameter
            try:
                inspect.getcallargs(fn)
                return wrapper
            except TypeError:
                try:
                    # If the above fails, try binding with a single tuple
                    # parameter. If this works, return the callback as is
                    inspect.getcallargs(fn, ())
                    return fn
                except TypeError:
                    raise ValueError(
                        'value must be a callable which accepts up to one '
                        'mandatory parameter')


    def _start_stop_thread(self):
        if self._callbacks and not self._callback_thread:
            print('starting callback thread')
            self._callback_event.clear()
            self._callback_thread = Thread(target=self._callback_run)
            self._callback_thread.daemon = True
            self._callback_thread.start()
        elif not self._callbacks and self._callback_thread:
            self._callback_event.set()
            self._callback_thread.join()
            self._callback_thread = None


    def _callback_run(self):
        while True:
            self.update()
            for event in self.get_events():
                callback = self._callbacks.get(event.button)
                if callback:
                    callback(event)
                callback = self._callbacks.get('*')
                if callback:
                    callback(event)


    @property
    def callback_a(self):
        """
        The function to be called when the A button is pressed or released. The function
        can either take a parameter which will be the `ButtonInputEvent` tuple that
        has occurred, or the function can take no parameters at all.
        """
        return self._callbacks.get(BUTTON_A)

    @callback_a.setter
    def callback_a(self, value):
        self._callbacks[BUTTON_A] = self._wrap_callback(value)
        self._start_stop_thread()


    @property
    def callback_b(self):
        """
        The function to be called when the B button is pressed or released. The function
        can either take a parameter which will be the `ButtonInputEvent` tuple that
        has occurred, or the function can take no parameters at all.
        """
        return self._callbacks.get(BUTTON_B)

    @callback_b.setter
    def callback_b(self, value):
        self._callbacks[BUTTON_B] = self._wrap_callback(value)
        self._start_stop_thread()


    @property
    def callback_top(self):
        """
        The function to be called when the TOP button is pressed or released. The function
        can either take a parameter which will be the `ButtonInputEvent` tuple that
        has occurred, or the function can take no parameters at all.
        """
        return self._callbacks.get(BUTTON_TOP)

    @callback_top.setter
    def callback_top(self, value):
        self._callbacks[BUTTON_TOP] = self._wrap_callback(value)
        self._start_stop_thread()


    @property
    def callback_bottom(self):
        """
        The function to be called when the BOTTOM button is pressed or released. The function
        can either take a parameter which will be the `ButtonInputEvent` tuple that
        has occurred, or the function can take no parameters at all.
        """
        return self._callbacks.get(BUTTON_BOTTOM)

    @callback_bottom.setter
    def callback_bottom(self, value):
        self._callbacks[BUTTON_BOTTOM] = self._wrap_callback(value)
        self._start_stop_thread()


    @property
    def callback_left(self):
        """
        The function to be called when the LEFT button is pressed or released. The function
        can either take a parameter which will be the `ButtonInputEvent` tuple that
        has occurred, or the function can take no parameters at all.
        """
        return self._callbacks.get(LEFT)

    @callback_left.setter
    def callback_left(self, value):
        self._callbacks[BUTTON_LEFT] = self._wrap_callback(value)
        self._start_stop_thread()


    @property
    def callback_right(self):
        """
        The function to be called when the RIGHT button is pressed or released. The function
        can either take a parameter which will be the `ButtonInputEvent` tuple that
        has occurred, or the function can take no parameters at all.
        """
        return self._callbacks.get(RIGHT)

    @callback_right.setter
    def callback_right(self, value):
        self._callbacks[BUTTON_RIGHT] = self._wrap_callback(value)
        self._start_stop_thread()


    @property
    def a_value(self):
        """Return the current debounced value of the A button."""
        return self._button_a.value


    @property
    def b_value(self):
        """Return the current debounced value of the B button."""
        return self._button_b.value


    @property
    def top_value(self):
        """Return the current debounced value of the TOP button."""
        return self._button_top.value


    @property
    def bottom_value(self):
        """Return the current debounced value of the BOTTOM button."""
        return self._button_bottom.value


    @property
    def left_value(self):
        """Return the current debounced value of the LEFT button."""
        return self._button_left.value


    @property
    def right_value(self):
        """Return the current debounced value of the RIGHT button."""
        return self._button_right.value
