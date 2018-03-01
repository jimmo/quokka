#!/bin/bash

# For setting up a new Quokka.
# Copies all libraries and one of the demos onto the board as main.py.
# e.g.   ./update.sh buttons-display-neopixels
# After copying everything, it connects the serial console so you can Ctrl-C/Ctrl-D.

# For ongoing development, rather than using this script, set up three terminals:
# 1. screen /dev/ttyACM0 115200
# 2. editor (e.g. main.py)
# 3. prompt $ cp main.py /media/PYBFLASH && sync
# Then for every update, run #3, then in #1:
#   - Ctrl-C (to stop current program)
#   - Ctrl-D (to force filesystem reload and start the new program)

cp quokka.py /media/PYBFLASH/
cp boot.py /media/PYBFLASH/
mkdir -p /media/PYBFLASH/drivers
cp drivers/*.py /media/PYBFLASH/drivers
cp demos/${1}.py /media/PYBFLASH/main.py
sync

screen /dev/ttyACM0 115200
