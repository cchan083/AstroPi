import os
import time

from internal.photography import Photography
from internal.tertiary import Tertiary
from internal.CONST import CONST

# Some code taken from the 'Calculating ISS speed with photos' but made it object oriented https://projects.raspberrypi.org/en/projects/astropi-iss-speed/0


class Speed:
    @staticmethod
    def calculate_speed(name_1: str, name_2: str, gsd: int = CONST.gsd):
        """Takes two photos, calculates distance and calculates speed."""
        Photography.take_picture(name=name_1, x=1920, y=1080)
        Photography.take_picture(name=name_2, x=1920, y=1080)


        """img1 = f'{home_dir}/photos/{name_1}-1.jpg'
        img2 = f'{home_dir}/photos/{name_2}-1.jpg'"""
        
        img1 = f'photos/{name_1}-1.jpg'
        img2 = f'photos/{name_2}-1.jpg'

        delta = Tertiary.get_time_delta(img1, img2)
        img1_cv, img2_cv = Tertiary.convert_to_cv(img1, img2)

        kp1, kp2, des1, des2 = Tertiary.calculate_features(img1_cv,
                                                           img2_cv,
                                                           CONST.feature_num)

        matches = Tertiary.calculate_matches(des1, des2)

        coords1, coords2 = Tertiary.find_matching_coordinates(kp1, kp2, matches)
        avg_dist = Tertiary.calculate_mean_distance(coords1, coords2)
        speed = Tertiary.calculate_speed(avg_dist, gsd, delta)

        return speed

    @staticmethod
    def average_speed():
        """Iterates through speed calculations and averages them."""
        speed_values = []
        for i in range(0, 9): # Iterate multiple times
            speed = Speed.calculate_speed(name_1=f'photo{i}', name_2=f'photo{i + 1}')
            speed_values.append(speed)
            time.sleep(10)  # Delay to soft reset camera
           
        total = 0
        for i in speed_values:
             total = total + i
        
        average_speed = total / len(speed_values)
             

        with open('result.txt', 'a') as f:
            f.write(f"{average_speed:.4f}") # Store result as string