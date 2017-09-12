"""Return commands from the keyboard.

Maps:
    * Left and right arrow = prev and next setting.
    * Up and down arrow = prev and next value (up = positive increase).
    * Space = Save.
"""
import os

import pyflightrepl.commands as commands


LEFT = 68 if os.name == 'posix' else 75
RIGHT = 67 if os.name == 'posix' else 77
UP = 65 if os.name == 'posix' else 72
DOWN = 66 if os.name == 'posix' else 80
SPACE = 32
ARROW_PRE = 91 if os.name == 'posix' else 224


def read_blocking():
    """Block on a new command, return it."""
    key = _getord()

    if key == SPACE:
        return commands.SAVE
    elif key == ARROW_PRE:  # For arrow keys
        key = _getord()
        if key == LEFT:
            return commands.PREV_SETTING
        elif key == RIGHT:
            return commands.NEXT_SETTING
        elif key == UP:
            return commands.INC_VALUE
        elif key == DOWN:
            return commands.DEC_VALUE


def _getord():
    return ord(_getch())


def _getch():
    """If Windows getch() available, use that. If not, use a Unix version.

    Thank you to: https://gist.github.com/payne92/11090057
    """
    try:
        import msvcrt
        return msvcrt.getch()
    except ImportError:
        import sys
        import tty
        import termios
        fileno = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fileno)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fileno, termios.TCSADRAIN, old_settings)
