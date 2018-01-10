#!/bin/bash
cp quokka.py /media/PYBFLASH/
cp boot.py /media/PYBFLASH/
mkdir -p /media/PYBFLASH/drivers
cp drivers/*.py /media/PYBFLASH/drivers
cp demos/${1}.py /media/PYBFLASH/main.py
sync

screen /dev/ttyACM0 115200
