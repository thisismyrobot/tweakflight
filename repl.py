"""An xFlight REPL built on top of pyflightcli.

Allows for an embedded hardware xFlight interface - in this case a RasPi.
"""
import os
import time

import tweakflightrepl.connection as connection
import tweakflightrepl.commands as commands
import tweakflightrepl.reverse as reverse

# If on posix (assume posix = raspi) then use LCD and encoders.
if os.name == 'posix':
    import tweakflightrepl.output.lcd as printer
    import tweakflightrepl.input.encoders as reader
else:
    import tweakflightrepl.output.console as printer
    import tweakflightrepl.input.keyboard as reader


class State(object):
    """The state of the REPL."""
    def __init__(self, settings, conn):
        self._conn = conn
        self._settings = dict(settings)
        self._setting_keys = sorted(self._settings.keys())
        self._setting_index = 0
        self._current_increment = 0

    @property
    def _current_key(self):
        return self._setting_keys[self._setting_index]

    @property
    def current_setting(self):
        return self._current_key

    @property
    def current_value(self):
        return self._settings[self._current_key]

    @property
    def current_increment(self):
        return self._current_increment

    def _next(self):
        self._settings[self._current_key] -= self.current_increment
        self._current_increment = 0

        self._setting_index = min(
            len(self._settings) - 1,
            self._setting_index + 1
        )

    def _prev(self):
        self._settings[self._current_key] -= self.current_increment
        self._current_increment = 0

        self._setting_index = max(
            0,
            self._setting_index - 1
        )

    def _increment(self):
        self._settings[self._current_key] += 1
        self._current_increment += 1

    def _decrement(self):
        self._settings[self._current_key] = max(0, self.current_value - 1)
        self._current_increment -= 1

    def _save(self):
        if self.current_increment == 0:
            return 'no change'
        self._current_increment = 0
        key = self.current_setting
        value = self.current_value
        cmd = 'set {} = {}'.format(key, value)
        result = self._conn.get(cmd)
        if result[0] != '{} set to {}'.format(key, value):
            return '{} invalid'.format(value)
        return '{} saved'.format(value)

    def execute(self, command):
        """Apply a command to the current state, updating it and optionally
        returning a message.
        """
        if command == commands.NEXT_SETTING:
            return self._next()
        elif command == commands.PREV_SETTING:
            return self._prev()
        elif command == commands.INC_VALUE:
            return self._increment()
        elif command == commands.DEC_VALUE:
            return self._decrement()
        elif command == commands.SAVE:
            return self._save()
        return 'error!'


def repl():
    """REPL."""
    printer.print_simple('Starting...')
    try:
        conn = connection.Serial()
    except:
        printer.print_simple('No drone detected!')
        return

    settings = reverse.read_analogues(conn)
    state = State(settings, conn)
    printer.print_state(state, '{} settings'.format(len(settings)))

    while True:
        command = reader.read_blocking()
        if command is None:
            continue
        message = state.execute(command)
        printer.print_state(state, message)


if __name__ == '__main__':
    while True:
        try:
            repl()
        except:
            printer.print_simple('Crashed! Retrying in 5s...')
        finally:
            time.sleep(5)
