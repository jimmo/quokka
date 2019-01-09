import neopixel
neo = neopixel.NeoPixel()

import quokka
import time
import math

MINUTE_MS = 60 * 1000

HEIGHT = quokka.display.height
WIDTH = quokka.display.width

METRONOME_TOP = 8
METRONOME_CURVE_HEIGHT = 24
METRONOME_WIDTH = WIDTH * (2/3)
METRONOME_X_OFFSET = WIDTH * (1/6)

bpm = 120
beat_duration_ms = MINUTE_MS / bpm
flash_duration_ms = beat_duration_ms / 4

last_beat_time = time.ticks_ms()
current_time = last_beat_time
current_beat = 0

metronome_cycle_start = last_beat_time

def reset():
  global last_beat_time, current_time, current_beat, metronome_cycle_start
  last_beat_time = time.ticks_ms()
  current_time = last_beat_time
  current_beat = 0
  metronome_cycle_start = last_beat_time
  start_flash_beat()

def next_beat():
  global last_beat_time, current_time, current_beat
  last_beat_time = current_time
  current_beat = (current_beat + 1) % 4

def start_flash_beat():
  global current_beat
  indexes = [current_beat, current_beat + 4]
  if current_beat == 0:
    indexes = range(8)

  neo.clear()
  for i in indexes:
    if i % 4 == 0:
      red, green, blue = 0, 64, 0
    if i % 4 == 1:
      red, green, blue = 0, 0, 64
    if i % 4 == 2:
      red, green, blue = 64, 0, 64
    if i % 4 == 3:
      red, green, blue = 64, 0, 0
    neo[i] = (red, green, blue)
  neo.show()

def finish_flash_beat():
  neo.clear()
  neo.show()

def change_bpm(amount):
  global MINUTE_MS, beat_duration_ms, bpm
  if bpm + amount > 0:
    bpm += amount
  beat_duration_ms = MINUTE_MS / bpm
  flash_duration_ms = beat_duration_ms / 4

def draw_bpm():
  global bpm
  quokka.display.text(str(bpm) + 'bpm', 5, 5, 1)

def draw_metronome():
  global current_time, metronome_cycle_start, beat_duration_ms
  completion_ms = time.ticks_diff(current_time, metronome_cycle_start)

  # Use sin to get a value that goes 0 -> 1.0 -> 0 -> -1.0 -> 0 smoothly
  # This gives us center, right, center, left, center, right, center, left etc
  # The full period is two beats, it hits right and left on half beats
  metronome_pos = math.sin((completion_ms / (beat_duration_ms/2)) * (math.pi/2))

  bottom_y = HEIGHT
  bottom_x = int(WIDTH/2)
  top_y = int(math.fabs(metronome_pos) * METRONOME_CURVE_HEIGHT) + METRONOME_TOP
  top_x = int(METRONOME_X_OFFSET + metronome_pos * (METRONOME_WIDTH/2) + (METRONOME_WIDTH/2))

  # top at full left will be x=METRONOME_X_OFFSET, y=METRONOME_CURVE_HEIGHT + METRONOME_TOP
  # top at center will be x=WIDTH/2, y=METRONOME_TOP
  # top at full right will be x=METRONOME_X_OFFSET + METRONOME_WIDTH, y=METRONOME_CURVE_HEIGHT + METRONOME_TOP

  # Draw the metronome
  quokka.display.line(bottom_x, bottom_y, top_x, top_y, 1)

  # Draw the center indicator
  quokka.display.line(int(WIDTH/2), 0, int(WIDTH/2), 8, 1)

  if completion_ms > (beat_duration_ms * 2):  # completed a full period
    metronome_cycle_start = current_time

def update_display():
  quokka.display.fill(0)  # clear the display
  draw_metronome()
  draw_bpm()
  quokka.display.show()  # show the display


# quokka.display.line(x1, y1, x2, y2, color)

start_flash_beat()
update_display()
while True:
  current_time = time.ticks_ms()
  update_display()

  # flash_duration after the last beat
  if time.ticks_diff(current_time, last_beat_time) > flash_duration_ms:
    finish_flash_beat()

  # beat_duration after the last beat
  if time.ticks_diff(current_time, last_beat_time) > beat_duration_ms:
    next_beat()
    start_flash_beat()

  if quokka.button_a.was_pressed():
    change_bpm(-10)
    reset()

  if quokka.button_b.was_pressed():
    change_bpm(10)
    reset()

  if quokka.button_c.was_pressed():
    change_bpm(-1)
    reset()

  if quokka.button_d.was_pressed():
    change_bpm(1)
    reset()
