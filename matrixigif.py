from PIL import Image, ImageDraw, ImageFont

width=64
height=32

emojiFont = ImageFont.truetype("./static/fonts/seguiemj.ttf", 24)


def makeStage():
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)
    return image

def makeText(text, x=0, y=10):
    global emojiFont
    stage = makeStage()
    layer = ImageDraw.Draw(stage);
    layer.text( (x, y), text, font=emojiFont, embedded_color=True)
    return stage

def animate(text):
    global width
    global height
    global emojiFont
    frames = []
    xplace = width
    textwidth, textheight = emojiFont.getsize(text)
    while xplace > (0-textwidth):
        frames.append(makeText(text, xplace, int((height-textheight)) ))
        xplace -= 5
    frame_one = frames[0]
    frame_one.save("stage.gif", format="GIF", append_images=frames, save_all=True, duration=100, loop=0)

def makeGif(text):
    animate(text)


# makeGif("🔴 Live Now twitch.tv/sfmoe")