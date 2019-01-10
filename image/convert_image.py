# Written by Stephen Davies
# Converts a .png to a format read by load_image for the Quokka board

from PIL import Image
import zlib
import argparse
from pathlib import Path

def calculate_dim(width, height):
  n_width, n_height = 128, int(height*128/width)
  if n_height > 64:
    n_width, n_height = int(width*64/height), 64
  return n_width, n_height

def convert_image(filename, width, height):
  image = Image.open(filename)

  if width is None or height is None:
    width, height = calculate_dim(*image.size)

  print(f"Resizing to: {width}x{height}")

  im_small = image.resize((width, height))
  # Convert resized image to black and white
  im_bw = im_small.convert('1')
  image_buf = im_bw.tobytes()
  compressed_im = zlib.compress(image_buf)
  # Note filename .qimz meaning zlib compressed quokka image
  out_filename = '{}.qimz'.format(filename)
  with open(out_filename, 'wb') as output_file:
    wh = bytearray([width, height])
    output_file.write(wh)
    output_file.write(compressed_im)
  print('Image converted! Upload {} to Quokka and use load_image.'.format(out_filename))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Convert an image to the quokka binary format.")
  parser.add_argument('filename', type=Path, help="Filename of image to convert")
  parser.add_argument('--width', type=int, help="Width of output image (display width is 128)", default=None)
  parser.add_argument('--height', type=int, help="Height of output image (display height is 64)", default=None)

  args = parser.parse_args()

  convert_image(args.filename, args.width, args.height)