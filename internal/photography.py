from picamzero import Camera  # Redundant on home machines, pre installed on the pi's
import os

class Photography:
    @staticmethod
    def set_resolution(x: int=2592,y: int=1944): #(2592, 1944 is the max of V1 Module)
        """Defines the resolution of the image"""
        cam = Camera()
        cam.still_size = (x, y)

    @staticmethod
    def take_picture(name, x: int = 2592, y: int=1944):
        """Takes two pictures, stores them in the home directory"""
        Photography.set_resolution(x,y)
        #home_dir = os.environ['HOME']
        """from pathlib import Path
        home_dir = Path(__file__).parent.resolve()"""
        cam = Camera()
        cam.capture_sequence(f"photos/{name}.jpg", num_images=1)