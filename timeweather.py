# 1st row 9x 5y 12px font
# 2nd row 9x 18y 12px font
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import pathlib
from urllib.request import urlopen
import io

from dotenv import load_dotenv
load_dotenv()
import os
openweatherAPIKEY = os.getenv("openweather")


import requests
import json


width=64
height=32
fontSize=12
working_dir = pathlib.Path(__file__).parent.absolute()
gif_folder = os.path.join(working_dir, "static/images/")
font_folder = os.path.join(working_dir, "static/fonts")
time_stage = "time_stage.gif"
gif_name = "stage.gif"
emojiFont = ImageFont.truetype(os.path.join(font_folder, "seguiemj.ttf"), fontSize)
stage_x = 9
lineone_y = 5
linetwo_y = 18

now = datetime.datetime.now()



def makeStage():
    image = Image.open(os.path.join(gif_folder, time_stage)).convert('RGBA')
    return image

def makeTime():
    global emojiFont
    frames = []
    text = ''
    hour = now.strftime('%-I')
    minute = now.strftime('%M')
    ampm = now.strftime('%p')
    numb_frames = 2
    linetwo = ""
    min_temp = ""
    max_temp = ""
    iconfile = ""
    if minute =="00" or minute=="15" or minute=="30" or minute=="45":
        min_temp, max_temp, icon = weather()
        weatherCache = open('weathercache.txt', 'w')
        linetwo = f"{min_temp}°|{max_temp}°"
        weatherCache.write(linetwo)
        weatherCache.write("\n")
        weatherCache.write(icon)
        weatherCache.close()
    else:

        weatherCache = open('weathercache.txt', 'r')
        cache = weatherCache.readlines()
        linetwo = cache[0]


    while numb_frames > 0:
        stage = makeStage()
        layer = ImageDraw.Draw(stage)
        if numb_frames == 2:
            text = f"{hour}:{minute} {ampm}"
        else:
            text = f"{hour} {minute} {ampm}"
        textwidth, textheight = emojiFont.getsize(text)
        linetwow, linetwoh = emojiFont.getsize(linetwo)

        new_x = int((width-textwidth)/2)
        linetwo_fixedX = int((width-linetwow)/2)+12
        layer.text( (new_x, lineone_y), text, font=emojiFont, embedded_color=True)
        weather_icon = Image.open(os.path.join(gif_folder, "outgif", "temp_weather.png"))
        stage.paste(weather_icon, (stage_x-4, int(linetwo_y/2)+5 ), weather_icon )
        layer.text( (linetwo_fixedX, linetwo_y), linetwo, font=emojiFont, embedded_color=True)
        frames.append(stage)
        numb_frames -= 1
    frame_one = frames[0]     
    frame_one.save(os.path.join(gif_folder, "outgif", gif_name), format="GIF", append_images=frames, save_all=True, duration=400, loop=0)

def weather():
    temp_max = 0
    temp_min = 0
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat=41&lon=-87&appid={openweatherAPIKEY}")
    json_data = response.json() if response and response.status_code == 200 else None
    if json_data and 'main' in json_data:
        temp_max = kelvfar(json_data["main"]["temp_max"])
        temp_min = kelvfar(json_data["main"]["temp_min"]) 
    icon = getIcon(json_data["weather"][0]["icon"])       
    return (temp_min, temp_max, json_data["weather"][0]["icon"])

def kelvfar(val):
    # kelvin conversion formula
    # (Kelvin − 273.15) × 1.8 + 32 = Farenheit
    # round(temp)
    conversion = (val - 273.15) * 1.8 + 32
    return round(conversion)

def getIcon(code):
    img_data = urlopen(f"https://openweathermap.org/img/wn/{code}.png").read()
    image = Image.open(io.BytesIO(img_data))
    image.thumbnail((15,15))
    image.save(os.path.join(gif_folder, "outgif", "temp_weather.png"))
    return True
    
makeTime()

