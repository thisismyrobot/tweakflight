"""An xflight REPL built on top of pyflightcli.

Allows for an embedded hardware xflight interface - in this case a RasPi.
"""
import pyflightcli.connection as connection
import pyflightrepl.reverse as reverse

# Change per hardware.
import pyflightrepl.output.console as printer
import pyflightrepl.input.keyboard as reader


def repl():
    """REPL."""
    conn = connection.Serial()

    analogue_commands = reverse.read_analogues(conn)

    printer.print('ready')

    while True:

        command = reader.read_blocking()

        if command is None:
            continue

        printer.print(command)

#        execute(conn, command)







if __name__ == '__main__':
    repl()
