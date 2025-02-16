import statistics

import os
import time

from internal.photography import Photography
from internal.tertiary import Tertiary
from internal.CONST import CONST

class Speed:
    @staticmethod
    def calculate_speed(name_1: str, name_2: str, gsd: int = CONST.gsd):
        """Takes two photos, calculates distance and calculates speed."""
        Photography.take_picture(name=name_1, x=1920, y=1080)
        Photography.take_picture(name=name_2, x=1920, y=1080)

        home_dir = os.environ['HOME']

        img1 = f'{home_dir}/photos/{name_1}-1.jpg'
        img2 = f'{home_dir}/photos/{name_2}-1.jpg'

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

            if 7 < speed < 8: # Scrub outliers from storage
                speed_values.append(speed)
                time.sleep(10)  # Delay to soft reset camera
            else:
                continue
        average_speed = statistics.mean(speed_values)

        with open('result.txt', 'w') as f:
            f.write(f"{average_speed:.4f}") # Store result as string