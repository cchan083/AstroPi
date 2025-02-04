# from exif import Image
# from datetime import datetime
# import cv2
# import math
# from phototaking import take_pictures
# import threading
# import os
# import queue
# import time
#
# ########################################################################
#
# Q = queue.Queue()
#
# class Worker(threading.Thread):
#     def __init__(self, function, identifier: int, *args, **kwargs) -> None:
#         super().__init__()
#         self.function = function
#         self.identifier = identifier
#         self.args = args
#         self.kwargs = kwargs
#         self.result = None  # Store result directly
#
#     def run(self) -> None:
#         self.result = self.function(*self.args, **self.kwargs)  # Execute function
#         Q.put((self.identifier, self.result))  # Store results in queue
#
# ########################################################################
#
# def execute_workers(worker_tasks):
#     workers = [Worker(func, i, *args) for i, (func, *args) in enumerate(worker_tasks, 1)]
#
#     for worker in workers:
#         worker.start()  # Start all threads
#
#     for worker in workers:
#         worker.join()  # Wait for all threads
#
#     return {worker.identifier: worker.result for worker in workers}
#
# ########################################################################
# ###  ================= SECONDARY ORDER FUNCTIONS =================   ###
# ########################################################################
#
# def get_time(path: str = None) -> datetime:
#     with open(path, 'rb') as image_file:
#         img = Image(image_file)
#         time_str = img.get("datetime_original")
#         time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')  # Extract timestamp
#
#     return time
#
#
# def cv_worker(img_path: str) -> cv2:
#     return cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)
#
#
# def feature_worker(sifter: cv2.SIFT, image: str) -> tuple:
#     keywords, descriptor = sifter.detectAndCompute(image, None)
#     return keywords, descriptor
#
#
# ########################################################################
# ###   ================= PRIMARY ORDER FUNCTIONS ==================   ###
# ########################################################################
#
#
# def time_delta(img_1: str, img_2: str) -> float:
#     results = execute_workers([
#         (get_time, img_1),
#         (get_time, img_2)])
#     return (results[2] - results[1]) . total_seconds()  # Cast delta to seconds
#
#
# def convert_to_cv(image_1: str, image_2: str) -> cv2:
#     results = execute_workers([
#         (cv_worker, image_1),
#         (cv_worker, image_2)])
#     return results[1], results[2]  # Return grayscale images
#
#
# def calculate_features(image_1: cv2, image_2: cv2, feature_number: int = 2000) -> tuple:
#     sift = cv2.SIFT_create(nfeatures=feature_number)
#     results = execute_workers([
#         (feature_worker, sift, image_1),
#         (feature_worker, sift, image_2)])
#     return *results[1], *results[2]
#
#
# def calculate_matches(descriptors_1, descriptors_2):
#     brute_force = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True) #Brute force matching
#     matches = brute_force.match(descriptors_1, descriptors_2)
#     matches = sorted(matches, key=lambda x: x.distance)
#
#     return matches
#
#
# def find_matching_coordinates(keypoints_1: list, keypoints_2: list, matches: list) -> tuple:
#
#     coordinates_1 = []
#     coordinates_2 = []
#
#     for match in matches:
#         image_1_idx = match.queryIdx
#         image_2_idx = match.trainIdx
#
#         (x1, y1) = keypoints_1[image_1_idx].pt
#         (x2,y2) = keypoints_2[image_2_idx].pt
#
#         coordinates_1.append((x1,y1))
#         coordinates_2.append((x2,y2))
#
#     return coordinates_1, coordinates_2
#
#
# def calculate_mean_distance(coordinates_1: list, coordinates_2: list) -> float:
#     all_distances = 0
#
#     merged_coordinates = list(zip(coordinates_1, coordinates_2))
#     for coordinate in merged_coordinates:
#         x_difference = coordinate[0][0] - coordinate[1][0]
#         y_difference = coordinate[0][1] - coordinate[1][1]
#         distance = math.hypot(x_difference, y_difference) # Pythagoras for the distance
#         all_distances = all_distances + distance
#
#     return all_distances / len(merged_coordinates)
#
#
# ########################################################################
# ###   ==================  MAIN ORDER FUNCTION  ===================   ###
# ########################################################################
#
#
# def main(verbose:bool=False) -> None:
#     take_pictures(1, name='photo_1', x=1920, y=1080)
#     print(datetime.now())
#     time.sleep(4)
#     take_pictures(1, name='photo_2', x=1920, y=1080)
#     print(datetime.now())
#     home_dir = os.environ['HOME']
#     image_1 = (f"{home_dir}/photo_1.jpg") #import the taking photos function from phototaking.py for 2 images
#     image_2 = (f"{home_dir}/photo_2.jpg")
#
#     # Calculate time elapsed
#     delta = time_delta(image_1, image_2)
#
#     image1, image2 = convert_to_cv(image_1, image_2)
#     keywords1, descriptors1, keywords2, descriptors2 = calculate_features(image1, image2)
#
#     matches = calculate_matches(descriptors1, descriptors2)
#     coord1, coord2 = find_matching_coordinates(keywords1, keywords2, matches)
#
#     average_feature_distance = calculate_mean_distance(coord1, coord2)
#
#     calculate_speed = lambda avg_dist, gsd, td: (avg_dist * gsd / 100000) / td
#     speed = calculate_speed(average_feature_distance, 12648, delta)
#
#     with open("result.txt", "w") as results:
#         results.write(f"{speed}")
#
#
# ########################################################################
#
# if __name__ == "__main__":
#     main(verbose=True)

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

    with open("results.txt", "a") as file:
        file.write(f"{os.listdir()}")

    img1, img2 = f'{home_dir}/{name_1}-1.jpg', f'{home_dir}/{name_2}-1.jpg'

    delta = get_time_delta(img1, img2)
    img1_cv, img2_cv = convert_to_cv(img1, img2)

    kp1, kp2, des1, des2 = calculate_features(img1_cv, img2_cv, 2000)
    matches = calculate_matches(des1, des2)

    if verbose:
        match_img = cv2.drawMatches(img1_cv, kp1, img2_cv, kp2, matches[:100], None)
        cv2.imshow('Matches', cv2.resize(match_img, (1600, 600)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    coords1, coords2 = find_matching_coordinates(kp1, kp2, matches)
    avg_dist = calculate_mean_distance(coords1, coords2)
    speed = calculate_speed(avg_dist, gsd, delta)
    
    
    return speed
    
def average_speed():
    speed_values = []
    for i in range(0,9):
        speed = main(name_1=f'photo{i}', name_2=f'photo{i+1}')
        
        if 7 < speed < 8:
            speed_values.append(speed)
            time.sleep(1)
        else:
            continue
    average_speed = mean(speed_values)
    
    with open('result.txt', 'w') as f:
        f.write(f"{average_speed:.4f}")

if __name__ == "__main__":
    main(verbose=False)