"""Input from a pair of rotary encoders.

Maps:
    * Left encoder turn = prev and next setting (CW = next setting).
    * Right encoder turn = prev and next value (CW = positive increase).
    * Both buttons pushed = Save.
"""
import collections
import queue

import RPi.GPIO as gpio

import tweakflightrepl.commands as commands


__SETUP = False
__CMD = queue.Queue()


# GPIO assignments for encoders, using Board pins. A or B is the 'channel' on
# the encoder, based on encoder documentation in 'hardware' directory.
LEFT_A = 38
LEFT_B = 40
LEFT_PUSH = 36

RIGHT_A = 35
RIGHT_B = 37
RIGHT_PUSH = 33


def setup_pins():
    """Set up the pins."""

    # Use Board Pin numbers
    gpio.setmode(gpio.BOARD)

    # All pins are pulled down as we take to GND on close.
    gpio.setup(LEFT_A, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(LEFT_B, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(LEFT_PUSH, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(RIGHT_A, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(RIGHT_B, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(RIGHT_PUSH, gpio.IN, pull_up_down=gpio.PUD_UP)


def track_encoder(pin_A, pin_B, cw_command, ccw_command):
    """Track an encoder."""
    data_buffer = collections.OrderedDict()
    cw_pattern = ((0, 1), (0, 0), (1, 0), (1, 1))
    ccw_oattern = ((1, 0), (0, 0), (0, 1), (1, 1))

    def step(_):
        """Handle a change to either command pin on the encoder."""
        current_a = gpio.input(pin_A)
        current_b = gpio.input(pin_B)

        # Dict keys can't duplicate, stripping noise. Order tells direction.
        data_buffer[(current_a, current_b)] = None

        if tuple(data_buffer.keys()) == cw_pattern:
            __CMD.put(cw_command)
        elif tuple(data_buffer.keys()) == ccw_oattern:
            __CMD.put(ccw_command)

        if current_a == current_b == 1 or len(data_buffer) == 4:
            data_buffer.clear()

    gpio.add_event_detect(pin_A, gpio.BOTH, callback=step)
    gpio.add_event_detect(pin_B, gpio.BOTH, callback=step)


def track_button_pair(pin_left_push, pin_right_push, push_command):
    """Track both pins being pushed."""
    def push(_):
        """Handle either button being pushed."""
        if gpio.input(pin_left_push) == gpio.input(pin_right_push) == 1:
            __CMD.put(push_command)

    gpio.add_event_detect(pin_left_push, gpio.BOTH, callback=push, bouncetime=300)
    gpio.add_event_detect(pin_right_push, gpio.BOTH, callback=push, bouncetime=300)


def read_blocking():
    """The function called by the REPL."""
    global __SETUP
    if not __SETUP:
        setup_pins()
        track_encoder(LEFT_A, LEFT_B, commands.NEXT_SETTING, commands.PREV_SETTING)
        track_encoder(RIGHT_A, RIGHT_B, commands.INC_VALUE, commands.DEC_VALUE)
        track_button_pair(LEFT_PUSH, RIGHT_PUSH, commands.SAVE)

        __SETUP = True

    return __CMD.get()
