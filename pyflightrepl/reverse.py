"""Reverse-engineer settings from the CLI."""
def dump_profiles(conn):
    """Iterate the profiles."""
    profile_settings = []

    for profile_i in range(3):
        conn.get('profile {}'.format(profile_i))

        for line in conn.get('dump profile'):
            profile_settings.append('p{}:{}'.format(profile_i, line))

        for rate_profile_i in range(3):
            conn.get('rateprofile {}'.format(rate_profile_i))
            for line in conn.get('dump rates'):
                profile_settings.append(
                    'p{}:rp{}:{}'.format(profile_i, rate_profile_i, line)
                )

    return profile_settings


def read_analogues(conn):
    """Try to return all the analogue settings."""
    analogues = []
    base_settings = conn.get('dump all')

    profile_settings = dump_profiles(conn)

    for setting in base_settings + profile_settings:

        tokens = setting.split(' ')
        if len(tokens) != 4:
            continue

        if tokens[0] != 'set':
            continue

        try:
            value = int(tokens[3])
        except ValueError:
            continue

        analogues.append((tokens[1], tokens[3]))

    return analogues
