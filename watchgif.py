from threading import Thread,Event
from time import sleep
import showgif
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import pathlib

working_dir = pathlib.Path(__file__).parent.absolute()
gif_folder = os.path.join(working_dir, "static/images/outgif")
gif_name = "stage.gif"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        threadEvent.set() #trigger finish
        thread.join() #wait for thread to finish

def showIt(event):
    while True:
        if event.isSet():
            return()
        showgif.display_gif(os.path.join(gif_folder, gif_name))

def on_file_change(action):
    if action.event_type == 'modified':
        global event
        event.set()

if __name__ == "__main__":
    change_handler = ChangeHandler()
    observer = Observer()

    threadEvent=Event()
    thread = Thread(target = showIt, args = (threadEvent, ) )
    thread.start()
    observer.schedule(change_handler, path=gif_folder, recursive=False)
    observer.start()
