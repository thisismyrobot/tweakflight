# PyFlightCli

Some basic python-based command-line tools to interact with the BetaFlight
(and CleanFlight and RaceFlight and etc and etc) command line interface.

## Install

You need Python 3.6.

    python3 -m venv venv
    venv\Scripts\activate
    pip install -r requirements

## Usage

To see commands:

    python cli.py

(Thank you python-fire!)

Playing with rate profiles:

    python cli.py rate-profile -- -h
    ...
    Docstring:   Set the profile from 0-2 or return the current one if omitted.

    Usage:       cli.py rate-profile [PROFILE]
                 cli.py rate-profile [--profile PROFILE]

    python cli.py rate-profile
    0

    python cli.py rate-profile 1

    python cli.py rate-profile
    1

## Limitations

Only tested against Betaflight 3.1.7 so far.

## Errata

I've used "xFlight" to refer to all the similar version so I don't have to
list them all.
