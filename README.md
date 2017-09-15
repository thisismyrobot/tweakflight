# TweakFlight

![Assembled hardware](hardware/header.jpg?raw=true "Assembled hardware")

A Raspberry Pi-based controller to tweak settings on Betaflight (and
compatible alternatives) via their terminal interface.

(Used to be part of PyFlightCli)

## Install

You need Python 3.6 on a Raspberry Pi.

    pip install -r requirements.txt

I'm using /dev/ttyAMA0 for the serial port, you'll need to allow access by
turning off the getty stuff (Google is your friend, this changes per Raspbian
version).

## Usage

To run it:

    python repl.py

## Hardware

TODO :(
