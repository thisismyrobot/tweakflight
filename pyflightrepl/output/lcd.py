"""LCD printer, heavily based on the Console printer."""
import serial

import console as console_printer


__BUFFER = []
__SER_LCD = serial.Serial('/dev/ttyAMA0', 38400)


def _flush():
    # clear
    __SER_LCD.write(b'\0xFE\0x01')

    __SER_LCD.write(__BUFFER[0])


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

    buffer_lines = (pretty_line_break(abbreviate(setting_words), 16) + [''] * 4)[:4]
    buffer_lines[2] = '-' * 16

    final_line = '{:^16}'.format(
        '{}{}'.format(
            state.current_value,
            ' ({:+})'.format(state.current_increment) if state.current_increment != 0 else '',
        )
    )
    buffer_lines[3] = final_line

    __BUFFER.clear()
    __BUFFER.extend(buffer_lines)
    __BUFFER.append(message if message is not None else '')

    _flush()
