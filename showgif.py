# code originally from https://github.com/poemusica/rpi-matrix-gif
import time
from PIL import Image, ImageSequence
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def get_frames(path):
    # Returns an iterable of gif frames.
    frames = []
    with Image.open(path) as gif:
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('RGB')
            frames.append(frame)
        return frames



# Configuration for the matrix


def display_gif(path):
    # """Displays gif frames on matrix."""
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.gpio_slowdown = 2
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
    matrix = RGBMatrix(options=options)
    
    while True:
        for frame in get_frames(path):
            matrix.SetImage(frame)
            time.sleep(frame.info['duration']/1000)

# if __name__ == '__main__':
#to start use entr > "sudo ls stage.gif | sudo python sfmoe.py"
#  display_gif("/home/sfmoe/hub75message/stage.gif")
