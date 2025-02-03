from exif import Image
from datetime import datetime
import cv2
import math
from phototaking import take_pictures
import threading
import os
import queue

########################################################################

Q = queue.Queue()

class Worker(threading.Thread):
    def __init__(self, function, identifier: int, *args, **kwargs) -> None:
        super().__init__()
        self.function = function
        self.identifier = identifier
        self.args = args
        self.kwargs = kwargs
        self.result = None  # Store result directly

    def run(self) -> None:
        self.result = self.function(*self.args, **self.kwargs)  # Execute function
        Q.put((self.identifier, self.result))  # Store results in queue

########################################################################

def execute_workers(worker_tasks):
    workers = [Worker(func, i, *args) for i, (func, *args) in enumerate(worker_tasks, 1)]

    for worker in workers:
        worker.start()  # Start all threads

    for worker in workers:
        worker.join()  # Wait for all threads

    return {worker.identifier: worker.result for worker in workers}

########################################################################
###  ================= SECONDARY ORDER FUNCTIONS =================   ###
########################################################################

def get_time(path: str = None) -> datetime:
    with open(path, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')  # Extract timestamp

    return time


def cv_worker(img_path: str) -> cv2:
    return cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)


def feature_worker(sifter: cv2.SIFT, image: str) -> tuple:
    keywords, descriptor = sifter.detectAndCompute(image, None)
    return keywords, descriptor


########################################################################
###   ================= PRIMARY ORDER FUNCTIONS ==================   ###
########################################################################


def time_delta(img_1: str, img_2: str) -> float:
    results = execute_workers([
        (get_time, img_1),
        (get_time, img_2)])
    return (results[2] - results[1]) . total_seconds()  # Cast delta to seconds


def convert_to_cv(image_1: str, image_2: str) -> cv2:
    results = execute_workers([
        (cv_worker, image_1),
        (cv_worker, image_2)])
    return results[1], results[2]  # Return grayscale images


def calculate_features(image_1: cv2, image_2: cv2, feature_number: int = 2000) -> tuple:
    sift = cv2.SIFT_create(nfeatures=feature_number)
    results = execute_workers([
        (feature_worker, sift, image_1),
        (feature_worker, sift, image_2)])
    return *results[1], *results[2]


def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True) #Brute force matching
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)

    return matches


def find_matching_coordinates(keypoints_1: list, keypoints_2: list, matches: list) -> tuple:

    coordinates_1 = []
    coordinates_2 = []

    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx

        (x1, y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt

        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))

    return coordinates_1, coordinates_2


def calculate_mean_distance(coordinates_1: list, coordinates_2: list) -> float:
    all_distances = 0

    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference) # Pythagoras for the distance
        all_distances = all_distances + distance

    return all_distances / len(merged_coordinates)


########################################################################
###   ==================  MAIN ORDER FUNCTION  ===================   ###
########################################################################


def main(verbose:bool=False) -> None:
    take_pictures(1, name='photo_1', x=1920, y=1080)
    take_pictures(1, name='photo_2', x=1920, y=1080)
    home_dir = os.environ['HOME']
    image_1 = (f"{home_dir}/photo_1.jpg") #import the taking photos function from phototaking.py for 2 images
    image_2 = (f"{home_dir}/photo_2.jpg") 

    # Calculate time elapsed
    delta = time_delta(image_1, image_2)

    image1, image2 = convert_to_cv(image_1, image_2)
    keywords1, descriptors1, keywords2, descriptors2 = calculate_features(image1, image2)

    matches = calculate_matches(descriptors1, descriptors2)
    coord1, coord2 = find_matching_coordinates(keywords1, keywords2, matches)

    average_feature_distance = calculate_mean_distance(coord1, coord2)

    calculate_speed = lambda avg_dist, gsd, td: (avg_dist * gsd / 100000) / td
    speed = calculate_speed(average_feature_distance, 12648, delta)

    with open("result.txt", "w") as results:
        results.write(f"{speed}")


########################################################################

if __name__ == "__main__":
    main(verbose=True)
