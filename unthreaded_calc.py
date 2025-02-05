from exif import Image
from datetime import datetime
import cv2
import math
from phototaking import take_pictures
import os
import time
from statistics import mean


def get_time(path: str) -> datetime:
    with open(path, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        return datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')


def get_time_delta(image_path_1: str, image_path_2: str) -> float:
    time_1 = get_time(image_path_1)
    time_2 = get_time(image_path_2)
    return (time_2 - time_1).seconds


def convert_to_cv(image_1, image_2):
    image_1_cv = cv2.cvtColor(cv2.imread(image_1), cv2.COLOR_BGR2GRAY)
    image_2_cv = cv2.cvtColor(cv2.imread(image_2), cv2.COLOR_BGR2GRAY)
    return image_1_cv, image_2_cv


def calculate_features(image_1, image_2, feature_number):
    sift = cv2.SIFT_create(nfeatures=feature_number)
    kp1, des1 = sift.detectAndCompute(image_1, None)
    kp2, des2 = sift.detectAndCompute(image_2, None)
    return kp1, kp2, des1, des2


def calculate_matches(des1, des2):
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)
    return sorted(matches, key=lambda x: x.distance)


def find_matching_coordinates(kp1, kp2, matches):
    coords1 = [kp1[m.queryIdx].pt for m in matches]
    coords2 = [kp2[m.trainIdx].pt for m in matches]
    return coords1, coords2


def calculate_mean_distance(coords1, coords2):
    total = 0.0
    for (x1, y1), (x2, y2) in zip(coords1, coords2):
        total += math.hypot(x2 - x1, y2 - y1)
    return total / len(coords1)


def calculate_speed(mean_dist, gsd, time_delta):
    distance_km = (mean_dist * gsd) / 100000  # Convert cm to km
    return distance_km / time_delta  # km/s


def main(name_1, name_2, verbose=False, gsd=12648):
    take_pictures(1, name=name_1, x=1920, y=1080)
    take_pictures(1, name=name_2, x=1920, y=1080)

    home_dir = os.environ['HOME']

    img1, img2 = f'{home_dir}/{name_1}-1.jpg', f'{home_dir}/{name_2}-1.jpg'

    delta = get_time_delta(img1, img2)
    img1_cv, img2_cv = convert_to_cv(img1, img2)

    kp1, kp2, des1, des2 = calculate_features(img1_cv, img2_cv, 2000)
    matches = calculate_matches(des1, des2)

    coords1, coords2 = find_matching_coordinates(kp1, kp2, matches)
    avg_dist = calculate_mean_distance(coords1, coords2)
    speed = calculate_speed(avg_dist, gsd, delta)

    return speed


def average_speed():
    speed_values = []
    for i in range(0, 9):
        speed = main(name_1=f'photo{i}', name_2=f'photo{i + 1}', verbose=False)

        if 7 < speed < 8:
            speed_values.append(speed)
            time.sleep(10)
        else:
            continue
    average_speed = mean(speed_values)

    with open('result.txt', 'w') as f:
        f.write(f"{average_speed:.4f}")


if __name__ == "__main__":
    average_speed()