"""Basic CLI interface."""
import fire
import pyflightcli.connection as connection


class PyFlightCli(object):
    """CLI for xFlight CLIs."""
    def __init__(self):
        self._conn = connection.Serial()

    @staticmethod
    def _make_dict(data):
        """Try to make a dict from CLI output."""
        output = {}
        for line in sorted(data):
            tokens = line.split(' ')
            if tokens[0] == 'set' and tokens[2] == '=':
                output[tokens[1]] = ' '.join(tokens[3:])
        return output

    def rates(self):
        """Return the current rate profile's rates."""
        dump = self._conn.get('dump rates')
        dump_dict = PyFlightCli._make_dict(dump)
        rates_dict = {}
        rates_dict['profile'] = int(dump[0].split(' ')[-1])
        rates_dict.update(dump_dict)
        return rates_dict

    def rate_profile(self, profile=None):
        """Set the profile from 0-2 or return the current one if omitted."""
        if profile is None:
            return int(self._conn.get('rateprofile')[0].split(' ')[-1])

        profile_idx = int(profile)
        if profile_idx < 0 or profile_idx > 2:
            raise Exception('Invalid rateprofile setting!')
        response = self._conn.get('rateprofile {}'.format(profile_idx))
        if response[0] != 'rateprofile {}'.format(profile_idx):
            raise Exception('Failed to set rateprofile!')


if __name__ == '__main__':
    fire.Fire(PyFlightCli)
