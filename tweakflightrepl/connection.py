"""The connection to the controller."""
import serial
import serial.tools.list_ports


MAX_READ = 40960
DETECT_TIMEOUT = 0.1
READ_TIMEOUT = 0.5


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
    def _read(conn, custom_read_timeout=None):
        old_timeout = conn.timeout
        try:
            if custom_read_timeout is not None:
                conn.timeout = custom_read_timeout
            data = conn.read(MAX_READ).decode()
        finally:
            conn.timeout = old_timeout
        return list(filter(None, map(str.strip, data.split('\r\n'))))

    @staticmethod
    def _get(conn, data, comments=False, custom_read_timeout=None):
        """Send and retrieve data."""
        Serial._write(conn, data)
        response = Serial._read(conn, custom_read_timeout)

        # Strip command echo.
        if response[0] == data:
            response = response[1:]

        if not comments:
            response = [line
                        for line
                        in response
                        if not line.startswith('#')]

        return response

    def get(self, data, comments=False, custom_read_timeout=None):
        """Send and retrieve data."""
        return Serial._get(self._conn, data, comments, custom_read_timeout)

    def current_port(self):
        """What port am I using?"""
        return self._conn.port

    def _find(self):
        """Try to find the port.

        Deliberately exclude the port on the GPIO, we're plugging in the
        controller to a USB port.
        """
        ports = [port
                 for port
                 in serial.tools.list_ports.comports()
                 if port.device != '/dev/ttyAMA0']

        for port in ports:
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
