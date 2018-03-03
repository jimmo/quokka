#!/bin/bash

# Copies one of the demos to the quokka as main,py
# e.g.   ./update.sh buttons-display-neopixels
# After copying everything, it connects the serial console so you can Ctrl-C/Ctrl-D.

# For setting up a new Quokka, pass the -u flag to the script.
# This copies all libraries and one of the demos onto the board as main.py.

# For ongoing development, rather than using this script, set up three terminals:
# 1. screen /dev/ttyACM0 115200
# 2. editor (e.g. main.py)
# 3. prompt $ cp {filename}.py /media/PYBFLASH/main.py && sync
# Then for every update, run #3, then in #1:
#   - Ctrl-C (to stop current program)
#   - Ctrl-D (to force filesystem reload and start the new program)

# If using an SD card with your quokka, update this volume name
VOL_NAME="PYBFLASH"

# If the -u flag is given, update the libraries
# Otherwise, only the main files are updated
if [ "$1" = "-u" ]; then
    cp quokka.py /media/$VOL_NAME/
    cp boot.py /media/$VOL_NAME/
    mkdir -p /media/$VOL_NAME/drivers
    cp drivers/*.py /media/$VOL_NAME/drivers/
    shift
fi
# Copy the demo onto the board
cp demos/${1}.py /media/$VOL_NAME/main.py
sync

screen /dev/ttyACM0 115200
