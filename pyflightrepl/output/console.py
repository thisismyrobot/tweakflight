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
    'declination': 'decln',
    'sensitivity': 'sens',
    'warning': 'warn',
}
__BUFFER = []


def _flush():
    os.system('cls')
    sys.stdout.write('\n'.join(__BUFFER))


def pretty_line_break(words, max_chars):
    """Tidily split the sentences over multiple lines.

    Return it as a list of lines.
    """
    if len(words) == 0:
        return []

    remaining_words = list(words)
    lines = [remaining_words.pop(0)]
    while len(remaining_words) > 0:
        next_word = remaining_words.pop(0)
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
