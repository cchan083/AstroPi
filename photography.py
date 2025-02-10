from exif import Image
from picamzero import Camera  # Redundant on home machines, pre installed on the pi's

from time import sleep
from datetime import datetime
import os

class Photography:
    @staticmethod
    def set_resolution(x: int=2592,y: int=1944): #(2592, 1944 is the max of V1 Module)
        home_dir = os.environ['HOME']
        cam = Camera()
        cam.still_size = (x, y)

    @staticmethod
    def take_pictures(num_images, name, x: int = 2592, y: int=1944): #num_images=x, interval(seconds)=y
        Photography.set_resolution(x,y)
        home_dir = os.environ['HOME']
        cam = Camera()
        cam.capture_sequence(f"{home_dir}/{name}.jpg", num_images=num_images)