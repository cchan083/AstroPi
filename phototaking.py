from exif import Image
from datetime import datetime
import cv2
import math
from picamzero import Camera #Make sure to instead sudo and python3-picamzero
from time import sleep
import os

#set resolution to 2592, 1944 (max resol of the V1 Module
home_dir = os.environ['HOME']
cam = Camera()
cam.still_size = (2592, 1944)
cam.preview_size = (1920, 1080)
cam = Camera()
cam.start_preview()

#def of setting resolution

# Keep the preview window open for 5 seconds
sleep(5)

cam = Camera() #view and rotate photos using flip camera.
cam.flip_camera(hflip=True)
cam.start_preview()
sleep(5)

cam.flip_camera(hflip=True, vflip=True) #flip 180 degrees.

cam = Camera()
cam.start_preview()
cam.take_photo("~/Desktop/new_image.jpg")
cam.stop_preview()

home_dir = os.environ['HOME'] #set the location of your home directory
cam = Camera()

#take photos.
cam.start_preview()
cam.take_photo(f"{home_dir}/Desktop/new_image.jpg") #save the image to your desktop
cam.stop_preview()

#capture multiple photos
home_dir = os.environ['HOME']
cam = Camera()

cam.start_preview()
cam.capture_sequence(f"{home_dir}/Desktop/sequence.jpg", num_images=3, interval=2)
cam.stop_preview()

#record a video
home_dir = os.environ['HOME']
cam = Camera()

cam.start_preview()
cam.capture_sequence(f"{home_dir}/Desktop/sequence.jpg", num_images=3, interval=2)
cam.stop_preview()

#add timestamp
home_dir = os.environ['HOME']
cam = Camera()

cam.start_preview()
cam.annotate(str(datetime.now()))
cam.take_photo(f"{home_dir}/Desktop/textOnPhoto.jpg")
cam.stop_preview()