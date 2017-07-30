"""Basic CLI interface."""
import os
import re

import fire
import pyflightcli.connection as connection


DUMP_ALL_TIMEOUT = 3  # Seems slower when doing a dump all


class PyFlightCli(object):
    """CLI for xFlight CLIs."""
    def __init__(self):
        self._conn = connection.Serial()

    @staticmethod
    def _make_dict(data, sort=True):
        """Try to make a dict from CLI output."""
        output = {}
        for line in sorted(data) if sort else data:
            tokens = line.split(' ')
            if tokens[0] == 'set' and tokens[2] == '=':
                output[tokens[1]] = ' '.join(tokens[3:]).strip()
        return output

    def port(self):
        """Return what port the CLI was detected on."""
        return self._conn.current_port()

    def pids(self):
        """Return the current profile's pids."""
        dump = self._conn.get('dump profile')

        pids_dict = {}
        pids_dict['profile'] = int(dump[0].split(' ')[-1])

        # Filter to just pid
        filtered_dump = [line
                         for line
                         in dump
                         if re.match('set [pid]_', line) is not None]

        def pid_sort_key(pid_key):
            """Manually sort to P-I-D but A-Z inside that."""
            order = {
                'p': 'a',
                'i': 'b',
                'd': 'c'
            }
            new_key = list(pid_key)
            new_key[4] = order[pid_key[4]]
            return ''.join(new_key)

        sorted_dump = sorted(filtered_dump, key=pid_sort_key)

        dump_dict = PyFlightCli._make_dict(sorted_dump, sort=False)
        pids_dict.update(dump_dict)
        return pids_dict

    def rates(self):
        """Return the current rate profile's rates."""
        dump = self._conn.get('dump rates')

        rates_dict = {}
        rates_dict['rateprofile'] = int(dump[0].split(' ')[-1])

        dump_dict = PyFlightCli._make_dict(dump)
        rates_dict.update(dump_dict)
        return rates_dict

    def rate_profile(self, rateprofile=None):
        """Set the rate profile from 0-2 or return the current one if omitted."""
        if rateprofile is None:
            return int(self._conn.get('rateprofile')[0].split(' ')[-1])

        rateprofile_idx = int(rateprofile)
        if rateprofile_idx < 0 or rateprofile_idx > 2:
            raise Exception('Invalid rateprofile setting!')
        response = self._conn.get('rateprofile {}'.format(rateprofile_idx))
        if response[0] != 'rateprofile {}'.format(rateprofile_idx):
            raise Exception('Failed to set rateprofile!')

    def profile(self, profile=None):
        """Set the profile from 0-2 or return the current one if omitted."""
        if profile is None:
            return int(self._conn.get('profile')[0].split(' ')[-1])

        profile_idx = int(profile)
        if profile_idx < 0 or profile_idx > 2:
            raise Exception('Invalid profile setting!')
        response = self._conn.get('profile {}'.format(profile_idx))
        if response[0] != 'profile {}'.format(profile_idx):
            raise Exception('Failed to set profile!')

    def dump(self):
        """Do a complete dump."""
        data = self._conn.get(
            'dump all',
            comments=True,
            custom_read_timeout=DUMP_ALL_TIMEOUT
        )
        return os.linesep.join(data)


if __name__ == '__main__':
    fire.Fire(PyFlightCli)
