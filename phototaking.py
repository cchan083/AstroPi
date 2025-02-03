from exif import Image
from datetime import datetime
import cv2
import math
from picamzero import Camera #Make sure to instead sudo and python3-picamzero
from time import sleep
import os

def set_resolution(x,y): #(2592, 1944 is the max of V1 Module)
    home_dir = os.environ['HOME']
    cam = Camera()
    cam.still_size = (x, y)
    #cam.preview_size = (1920, 1080)
    #cam = Camera()
    #cam.start_preview()
    
def keep_window_open(x):
    sleep(x)
    
def take_pictures(num_images, interval, name, x, y): #num_images=x, interval(seconds)=y
    set_resolution(x,y)
    home_dir = os.environ['AstroPi']
    cam = Camera()
    cam.start_preview()
    cam.capture_sequence(f"{home_dir}/Photos/sequence.jpg", num_images=num_images, interval=interval)
    cam.stop_preview()

if __name__ == "__main__":
    set_resolution()
    keep_window_open()
    take_pictures()
    