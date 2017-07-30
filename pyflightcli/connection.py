"""The connection to the controller."""
import serial
import serial.tools.list_ports


MAX_READ = 4096
DETECT_TIMEOUT = 0.1
READ_TIMEOUT = 2


class Serial(object):
    """A serial connection to an xFlight compatible CLI."""
    def __init__(self, baud=115200):
        self._baud = baud
        port = self._find()
        if port is None:
            raise Exception('Controller not found!')
        self._conn = serial.Serial(port, baud, timeout=READ_TIMEOUT)

    @staticmethod
    def _knock(conn):
        """Say knock-knock to a port."""
        response = Serial._get(conn, '#', comments=True)
        return response[0] == '#'

    @staticmethod
    def _write(conn, data):
        conn.write('{}\r\n'.format(data).encode())

    @staticmethod
    def _read(conn):
        data = conn.read(MAX_READ).decode()
        return list(filter(None, map(str.strip, data.split('\r\n'))))

    @staticmethod
    def _get(conn, data, comments=False):
        """Send and retrieve data."""
        Serial._write(conn, data)
        response = Serial._read(conn)

        # Strip command echo.
        if response[0] == data:
            response = response[1:]

        if not comments:
            response = [line
                        for line
                        in response
                        if not line.startswith('#')]

        return response

    def get(self, data, comments=False):
        """Send and retrieve data."""
        return Serial._get(self._conn, data, comments)

    def _find(self):
        """Try to find the port."""
        ports = list(serial.tools.list_ports.comports())

        # Reversing as the port is virtually never COM1.
        for port in sorted(ports, reverse=True):
            try:
                conn = serial.Serial(
                    port.device,
                    self._baud,
                    timeout=DETECT_TIMEOUT
                )
                if Serial._knock(conn):
                    conn.close()
                    return conn.port
            except:
                continue
