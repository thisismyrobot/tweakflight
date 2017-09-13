"""Input from a pair of rotary encoders."""
import collections

import RPi.GPIO as gpio


# GPIO assignments for encoders, using Board pins. A or B is the 'channel' on
# the encoder, based on encoder documentation in 'hardware' directory.
LEFT_A = 38
LEFT_B = 40
LEFT_PUSH = 36


def setup():
    """Set up the pins."""

    # Use Board Pin numbers
    gpio.setmode(gpio.BOARD)

    # All pins are pulled down as we take to GND on close.
    gpio.setup(LEFT_A, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(LEFT_B, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(LEFT_PUSH, gpio.IN, pull_up_down=gpio.PUD_UP)


def track_encoder(pin_A, pin_B, pin_push):
    """Track an encoder."""

    # Encoder
    data_buffer = collections.OrderedDict()
    cw = ((0, 1), (0, 0), (1, 0), (1, 1))
    ccw = ((1, 0), (0, 0), (0, 1), (1, 1))

    def step(_):
        current_a = gpio.input(pin_A)
        current_b = gpio.input(pin_B)

        # Dict keys can't duplicate, stripping noise. Order tells direction.
        data_buffer[(current_a, current_b)] = None

        if tuple(data_buffer.keys()) == cw:
            print('CW!')
        elif tuple(data_buffer.keys()) == ccw:
            print('CCW!')

        if current_a == current_b == 1 or len(data_buffer) == 4:
            data_buffer.clear()

    gpio.add_event_detect(pin_A, gpio.BOTH, callback=step)
    gpio.add_event_detect(pin_B, gpio.BOTH, callback=step)

    # Push button
    def push(_):
        print('push!')

    gpio.add_event_detect(LEFT_PUSH, gpio.FALLING, callback=push, bouncetime=300)

    input()


if __name__ == '__main__':
    setup()
    track_encoder(LEFT_A, LEFT_B, LEFT_PUSH)
