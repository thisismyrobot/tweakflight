"""Reverse-engineer settings from the CLI."""
def read_analogues(conn):
    """Try to return all the analogue settings."""
    analogues = []

    # Deliberately use the current profile + rateprofile.
    raw_settings = conn.get('dump', custom_read_timeout=3)

    for setting in raw_settings:

        tokens = setting.split(' ')

        if len(tokens) != 4:
            continue

        if tokens[0] != 'set':
            continue

        try:
            value = int(tokens[3])
        except ValueError:
            continue

        analogues.append((tokens[1], value))

    return analogues
