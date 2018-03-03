#!/bin/bash

# Copies a file to the quokka as main.py (and optionally adds all the quokka libraries).
# e.g.   ./update.sh demos/buttons-display-neopixels.py
# After copying everything, it connects the serial console so you can Ctrl-C/Ctrl-D.

# For setting up a new Quokka, pass the -u flag to the script.
# This copies all libraries and the selected file as as main.py.

# Disable connecting the serial console with -n

# For ongoing development, the workflow is to set up three terminals:
# 1. screen /dev/ttyACM0 115200
# 2. editor (e.g. path-to-my-program.py)
# 3. ./update.sh -n path-to-my-program.py
# Then for every update, run #3, then in #1:
#   - Ctrl-C (to stop current program)
#   - Ctrl-D (to force filesystem reload and start the new program)

# Check if we are on a mac
if [ `uname` = "Darwin" ]; then
    VOL_DIR="Volumes"
    OSX=1
else
    VOL_DIR="media"
    OSX=0
fi

# If using an SD card with your quokka, update this volume name
VOL_NAME="PYBFLASH"

# If the -u flag is given, update the libraries
# Otherwise, only the main files are updated
if [ "$1" = "-u" ]; then
    cp quokka.py /$VOL_DIR/$VOL_NAME/
    cp boot.py /$VOL_DIR/$VOL_NAME/
    mkdir -p /$VOL_DIR/$VOL_NAME/drivers
    cp drivers/*.py /$VOL_DIR/$VOL_NAME/drivers/
    shift
fi

CONNECT_SERIAL=1
# If the -n flag is given, remember to skip the serial console
if [ "$1" = "-n" ]; then
    CONNECT_SERIAL=0
    shift
fi

# If there is no argument given, copy main.py, otherwise copy the named demo
if [ $# -eq 0 ]; then
    cp main.py /$VOL_DIR/$VOL_NAME/main.py
else
    # Copy the argument onto the board
    cp ${1} /$VOL_DIR/$VOL_NAME/main.py
fi
sync

if [ $CONNECT_SERIAL -eq 1 ]; then
    if [ $OSX -eq 0 ]; then
        screen /dev/ttyACM0 115200
    else
        screen $(ls /dev/tty.usbmodem* | head -n1) 115200
    fi
fi
