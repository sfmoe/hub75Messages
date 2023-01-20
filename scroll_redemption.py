from PIL import Image, ImageSequence, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import os
import pathlib
import io
from urllib.request import urlopen
import re
from threading import Thread,Event



width=64
height=32
fontSize=24
working_dir = pathlib.Path(__file__).parent.absolute()
gif_folder = os.path.join(working_dir, "static/images/outgif")
font_folder = os.path.join(working_dir, "static/fonts")
gif_name = "newstage.gif"
urlREGEX = r'(https?://[^\s]+)'
passes = 2



separateUrls  = []

frame_master = []




# create_image is from https://github.com/FiniteSingularity/rpi-rgb-matrix-server/blob/main/utils.py
# finiteSingularity is awesome

def create_image(url): 
    img_data = urlopen(url).read()
    image = Image.open(io.BytesIO(img_data))

    image_dat = {
        "image": image,
        "frames": [],
        "current_frame": 0,
        "current_frame_start": 0,
    }
    for frame_num in range(0, getattr(image, "n_frames", 1)):
        image.seek(frame_num)
        duration = image.info.get('duration', 0)

        image_rgba = image.convert(mode='RGBA')
        frame = Image.new('RGB', image.size)
        frame.paste(image_rgba, mask=image_rgba)
        image_dat["frames"].append({"frame": frame, "duration": duration})
    
    return image_dat


def create_text(text):
    frames = []
    emojiFont = ImageFont.truetype("./static/fonts/seguiemj.ttf", 24)
    width, height = emojiFont.getsize(text)
    frame = Image.new("RGB", size=(width, 32))
    draw = ImageDraw.Draw(frame)
    draw.text((0,4), text, font=emojiFont, embedded_color=True)
    frames.append(frame)
    return frames


def scroll():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.gpio_slowdown = 2
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    matrix = RGBMatrix(options=options)
    double_buffer = matrix.CreateFrameCanvas()
    

    x_offset = 129
    last_x_change = 0
    current_pass = 0
    x_t_length = 16

    for idxportion, portion in enumerate(separateUrls):
        if(re.match(urlREGEX, portion) is not None):
            # convert to emote
            frame_master.append(create_image(portion))
        else:
            frame_master.append(create_text(portion))

    current_frame  = 0
    while current_pass < passes:
        message_width = 0
        double_buffer.Clear()
        current_time = int(round(time.time() * 1000))
        dt = current_time - last_x_change

        if dt > x_t_length:
            dx = -1
            last_x_change = current_time
        else:
            dx = 0
            
        for indx, x in enumerate(frame_master):
            if isinstance(x, list):
                #this is text frame
                w, h = x[0].size
                y_offset = 5
                double_buffer.SetImage(x[0], message_width + x_offset, y_offset)
                message_width += w
            
            if isinstance(x, dict):
                #this is emote frame
                frames = x["frames"]
                frame = ''
                if len(frames) > 1:
                    frame_index = (frame_master[indx]["current_frame"] +1 ) % len(frames)                    
                    frame = frames[frame_index]["frame"]
                    dt = current_time - frame_master[indx]["current_frame_start"]
                    max_dt = frames[frame_index]["duration"]

                    if (frame_index+1) > len(frames):
                        frame_master[indx]["current_frame"] = 0
                    else:
                        if dt > max_dt:
                            frame_master[indx]["current_frame"] = frame_index + 1
                            frame_master[indx]["current_frame_start"] = current_time


                        
                else:
                    frame = frames[0]["frame"]
                double_buffer.SetImage(frame, x_offset + message_width + 2, 7)
                message_width += 32
                # print((frame_index, current_frame))


           


        double_buffer = matrix.SwapOnVSync(double_buffer)
        x_offset += dx
        if x_offset < -message_width:
            x_offset = 128
            current_pass += 1
    

    

def start(text):
    global separateUrls
    separateUrls = re.split(urlREGEX, text)
    thread = Thread(target = scroll )
    thread.start()
    thread.join()

# start("this is a test https://static-cdn.jtvnw.net/emoticons/v2/1/default/dark/1.0 for 🤘 https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_f36f3cd50db149489e945b9d7436412f/default/light/1.0 thjs ac")