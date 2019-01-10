import framebuf
import drivers.series
from quokka import *

class Chart():
  def __init__(self,
    display=None,
    values=[], max_value_count=50,
    label=None, y_labels=True, y_label_width=4,
    start_x=None, end_x=None,
    start_y=None, end_y=None):

    self.display = display
    self.char_width, self.char_height = 8, 8
    self.values = drivers.series.BoundedSeries(max_value_count, values,
                                       y_label=label,
                                       min_x=start_x, max_x=end_x,
                                       min_y=start_y, max_y=end_y)

    self.y_labels = y_labels
    self.y_label_width = y_label_width

    self.screen_start_x = len(self.values.y_label)*8 + 1 if self.values.y_label is not None else 0
    self.screen_end_x = self.display.width - (self.y_label_width*self.char_width + 1) if self.y_labels else self.display.width
    self.screen_start_y = 0
    self.screen_end_y = self.display.height

  def push(self, value):
    self.values.push(value)

  def scale(self, x=None, y=None):
    # Get range of values
    start_x = 0
    end_x = len(self.values)
    start_y = self.values.min_y
    end_y = self.values.max_y
    range_x = 1 if end_x - start_x == 0 else end_x - start_x
    range_y = 1 if end_y - start_y == 0 else end_y - start_y
    screen_range_x = self.screen_end_x - self.screen_start_x
    screen_range_y = self.screen_end_y - self.screen_start_y

    if x != None:
      return self.screen_start_x + int((x - start_x)/range_x * screen_range_x)
    if y != None:
      return self.screen_start_y + int((y - start_y)/range_y * screen_range_y)

  def show(self):
    # Draw the values
    self.display.fill(1)
    prev_x, prev_y = 0, self.values[0] if self.values else 0
    for x, y in enumerate(self.values):
      self.display.line(self.scale(x=prev_x), self.scale(y=prev_y), self.scale(x=x), self.scale(y=y), 0)
      prev_x, prev_y = x, y

    # Draw the labels
    if self.values.y_label:
      y = self.display.height//2
      self.display.text(self.values.y_label, 0, y, 0)

    if self.y_labels and self.values:
      self.display.text(str(min(self.values)).center(self.y_label_width), self.screen_end_x+1, 0, 0)
      self.display.text(str(self.values[-1]).center(self.y_label_width), self.screen_end_x+1, self.display.height//2, 0)
      self.display.text(str(max(self.values)).center(self.y_label_width), self.screen_end_x+1, self.display.height - self.char_height, 0)

    # Show the chart
    self.display.show()


chart = Chart(display)
while True:
  x,y,z = accelerometer.x, accelerometer.y, accelerometer.z
  chart.push(x)
  chart.show()
  sleep(100)
