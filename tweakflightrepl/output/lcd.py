"""LCD printer, heavily based on the Console printer."""
import serial

import tweakflightrepl.output.console as console_printer


__BUFFER = []

# This is hard-coded based on my hardware setup.
__SER_LCD = serial.Serial('/dev/ttyAMA0', 38400)


def _flush():
    # clear
    __SER_LCD.write(b'\xfe\x01')

    for line in __BUFFER:
        __SER_LCD.write('{0: <20}'.format(line).encode())

def pretty_line_break(words, max_chars):
    """Tidily split the sentences over multiple lines.

    Return it as a list of lines.
    """
    return console_printer.pretty_line_break(words, max_chars)


def abbreviate(words):
    """Shorten some words."""
    return console_printer.abbreviate(words)


def print_state(state, message=None):
    """Format current state and print to console.
    """
    setting_words = state.current_setting.replace('_', ' ').split(' ')

    buffer_lines = (pretty_line_break(abbreviate(setting_words), 20) + [''] * 4)[:4]
    buffer_lines[2] = '-' * 20

    final_line = '{:^20}'.format(
        '{}{}{}'.format(
            state.current_value,
            ' ({:+})'.format(state.current_increment) if state.current_increment != 0 else '',
            ' ({})'.format(message) if message is not None else ''
        )
    )
    buffer_lines[3] = final_line

    __BUFFER.clear()
    __BUFFER.extend(buffer_lines)

    _flush()
