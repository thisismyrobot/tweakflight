"""Console printer."""
import os
import sys


def print_state(state, message=None):
    """Format current state and print to console."""
    current_setting = state.current_setting
    setting_value = state.current_value

    output = '{}: {}\n'.format(current_setting, setting_value)
    if message is not None:
        output += '{}\n'.format(message)

    sys.stdout.write('-----------------\n')
    sys.stdout.write(output)
