from PIL import Image, ImageDraw, ImageFont, ImageSequence
import os
import pathlib
import io
from urllib.request import urlopen
import re

width=64
height=32
fontSize=24
working_dir = pathlib.Path(__file__).parent.absolute()
gif_folder = os.path.join(working_dir, "static/images/outgif")
font_folder = os.path.join(working_dir, "static/fonts")
gif_name = "stage.gif"
redemption_name = "redemption.gif"
urlREGEX = r'(https?://[^\s]+)'

emojiFont = ImageFont.truetype(os.path.join(font_folder, "seguiemj.ttf"), fontSize)

def makeStage():
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    return image

def create_text(text):
    global emojiFont
    lw, lh = emojiFont.getsize(text)
    frame = Image.new("RGB", size=(lw, height))
    layer = ImageDraw.Draw(frame);
    y = int(height - lh)
    layer.text( (0, y), text, font=emojiFont, embedded_color=True)
    return frame

# create_image is from https://github.com/FiniteSingularity/rpi-rgb-matrix-server/blob/main/utils.py
# finiteSingularity is awesome

def create_image(url): 
    img_data = urlopen(url).read()
    image = Image.open(io.BytesIO(img_data))
    image.thumbnail((height,height))
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

def handleURLS(text):
    # returns a list with images and text in order
    frames = []
    totalWidth = 0
    separateUrls = re.split(urlREGEX, text)
    for idxportion, portion in enumerate(separateUrls):
        if(re.match(urlREGEX, portion) is not None):
            # convert to emote
            em = create_image(portion);
            frames.append(em)
            emw, emh  = em["image"].size
            totalWidth += emw+4
        else:
            tx = create_text(portion)
            frames.append(tx)
            txw, txh = tx.size
            totalWidth += txw+4
    return {"frames": frames, "width": totalWidth}

def combineImages(frames):
    global height
    allFrames = frames["frames"]
    animated = []
    maxframes = 0
    xframes = []
    fwidth  = frames["width"]
    masterImage = Image.new("RGB", (fwidth, height))
    location = 0
    for indx, x in enumerate(allFrames):
        # print(type(x))
        if isinstance(x, dict):
            x["image"].thumbnail((28,28))
            dw, dh = x["image"].size  
            animated.append({"frames": x["frames"], "location": location, "currentframe": 0})
            if len(x["frames"]) > maxframes:
                maxframes = len(x["frames"])
            location += dw
        else:
            pw, ph = x.size
            masterImage.paste(x,(location, 0))
            location += pw
    i = 0
    while i < maxframes-1:
        masterCopy = masterImage.copy()
        for ai, ax in enumerate(animated):
            if ax["currentframe"] <= len(ax["frames"])-1:
                masterCopy.paste(ax["frames"][ax["currentframe"]]["frame"], (ax["location"], 2))
                animated[ai]["currentframe"] += 1
            else:
                animated[ai]["currentframe"] = 0
                
            
            xframes.append(masterCopy)
        i+=1

    frame_one = xframes[0]
    frame_one.save(os.path.join(gif_folder, gif_name), format="GIF", append_images=xframes, save_all=True, duration=0, loop=0)
    return xframes


def animate(text):
    handledURLs = handleURLS(text)
    combineImages(handledURLs)



# animate("s🔴 ")
animate("this is a massive long 😂 test message with lots of words for scrolling 🔴 https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_f36f3cd50db149489e945b9d7436412f/default/light/1.0 https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_b33dc0a5aebc4f62959b4c4fc7c5e33a/default/light/1.0")