# HUB75 Adafruit Animated Panel

Using this to create animated gifs of messages to be used with a raspberry pi with attached 64x32 HUB75 panel.

it has two parts:

- A service that runs flask server that you can create messages with
- A service that has a file watcher for the gif, if it changes it reruns the panel display

caveat: 
- you need to provide your own font file ;)

## TODO
------

- write an install script that doesnt have my user folder hard coded into the service files.

- handle urls for gifs to input

- multiline is broken as hell ( sizing of font )

- static is pretty broken too need to resize image to fit in stage

## Sample Gif output with emoji
---

![test ouput from script](static/images/test_output.gif "test ouput from script")
