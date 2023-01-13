from PIL import Image, ImageDraw, ImageFont
import os
import pathlib

width=64
height=32
fontSize=24
working_dir = pathlib.Path(__file__).parent.absolute()
gif_folder = os.path.join(working_dir, "static/images/outgif")
font_folder = os.path.join(working_dir, "static/fonts")
gif_name = "stage.gif"

emojiFont = ImageFont.truetype(os.path.join(font_folder, "seguiemj.ttf"), fontSize)



def makeStage():
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)
    return image

def makeText(text="sample text", x=0, y=10, multiline=False):
    global emojiFont
    stage = makeStage()
    layer = ImageDraw.Draw(stage);
    if multiline:
        emojiFont = ImageFont.truetype("./static/fonts/seguiemj.ttf", 20)
        textlist = list(text)
        listlen = int(len(textlist)/2)
        textlist.insert( listlen, "\n" )
        layer.multiline_text((x, 4), "".join(textlist), font=emojiFont, embedded_color=True, align="left")
    else:
        layer.text( (x, y), text, font=emojiFont, embedded_color=True)
    return stage

def static(text, multiline):
    global width
    global height
    frames = []
    for number in range(1, 25):
        textwidth, textheight = emojiFont.getsize("tesT".join(text))
        frames.append(makeText(text, 0, int((height-textheight)), multiline))
    frame_one = frames[0]
    frame_one.save(os.path.join(gif_folder, gif_name), format="GIF", append_images=frames, save_all=True, duration=100, loop=0)

def animate(text, multiline):
    # only scrolls if text goes out of bounds
    global width
    global height
    global emojiFont
    frames = []
    xplace = width
    textwidth, textheight = emojiFont.getsize(text)
    if textwidth-15 < width:
        for number in range(1, 25):
            frames.append(makeText(text, multiline))
    else:
        while xplace > (0-textwidth):
            frames.append(makeText(text, xplace, int((height-textheight)), multiline ))
            xplace -= 5
    frame_one = frames[0]
    frame_one.save(os.path.join(gif_folder, gif_name), format="GIF", append_images=frames, save_all=True, duration=100, loop=0)

def makeGif(text, scrolltype, multiline):
    if (scrolltype=="scroll"):
        animate(text, multiline)
    elif(scrolltype=="static"):
        static(text, multiline)


# makeGif("🔴 Live Now twitch.tv/sfmoe", "scroll", True)
