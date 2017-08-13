"""Console printer."""
import os
import sys


SUBSTITUTIONS = {
    'deadband': 'dband',
    'throttle': 'thr',  # Used elsewhere in settings.
    'displayport': 'dport',
    'failsafe': 'fsafe',
    'command': 'cmd',
    'control': 'ctrl',
}
__BUFFER = []


def _flush():
    os.system('cls')
    sys.stdout.write('\n'.join(__BUFFER))


def pretty_line_break(words, max_chars=16):
    """Tidily split the sentences over multiple lines.

    Return it as a list of lines.
    """
    lines = [words.pop(0)]
    while len(words) > 0:
        next_word = words.pop(0)
        current_line = lines[-1]
        candidate = ' '.join((current_line, next_word))
        if len(candidate) <= max_chars:
            lines[-1] = candidate
        else:
            lines.append(next_word)
    return lines


def abbreviate(words):
    """Shorten some words."""
    abbreviated_words = []
    for word in words:
        try:
            abbreviated_words.append(SUBSTITUTIONS[word])
        except KeyError:
            abbreviated_words.append(word)
    return abbreviated_words


def print_state(state, message=None):
    """Format current state and print to console.

    Somewhat simulate a 16x4 LCD because that's what I'll use next.
    """
    setting_words = state.current_setting.replace('_', ' ').split(' ')
    setting_value = state.current_value

    abbreviated_words = abbreviate(setting_words)
    setting_lines = pretty_line_break(abbreviated_words)

    __BUFFER.clear()
    __BUFFER.extend(setting_lines)
    __BUFFER.append(str(setting_value))
    __BUFFER.append(message if message is not None else '')

    _flush()
