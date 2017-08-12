"""Console printer."""
import collections
import os
import sys


__BUFFER = collections.defaultdict(str)

def _flush():
    os.system('cls')
    sys.stdout.write('{}\n'.format(__BUFFER['top_line']))
    sys.stdout.write('{}\n'.format(__BUFFER['bottom_line']))


def print_state(state, message=None):
    """Format current state and print to console."""
    current_setting = state.current_setting
    setting_value = state.current_value

    __BUFFER['top_line'] = '{}: {}'.format(current_setting, setting_value)
    __BUFFER['bottom_line'] = message if message is not None else ''

    _flush()
