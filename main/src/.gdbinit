file main.elf
target extended-remote /dev/ttyACM0
monitor swdp_scan
attach 1
load
run
