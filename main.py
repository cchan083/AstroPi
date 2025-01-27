from exif import Image
from datetime import datetime
import cv2
import math

# 3 . 4 6 2 2

# TODO
# Planning other ways - google coral
# Prewrite the Photos camera module - Billy
# Thread - Euan


def camera(): # billy do this or I will find you <3
    pass


def get_time(path: str) -> datetime:
    with open(path, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S') # Getting the date time of image

    return time


def get_time_delta(image_path_1: str, image_path_2: str) -> float:

    # Scrape time metadata from the two images
    time_1 = get_time(path=image_path_1)
    time_2 = get_time(path=image_path_2)

    time_delta = time_2 - time_1
    return time_delta.seconds  # Cast time difference to seconds


def convert_to_cv(image_1, image_2):

    # CV image construction
    image_1_cv = cv2.cvtColor(
        cv2.imread(image_2), cv2.COLOR_BGR2GRAY)
    image_2_cv = cv2.cvtColor(
        cv2.imread(image_1), cv2.COLOR_BGR2GRAY)

    # x, y, width, height = 500, 500, 4000, 4000
    # image_1_cv = image_1_cv[y:y+height, x:x+width]
    # image_2_cv = image_2_cv[y:y+height, x:x+width]
    return image_1_cv, image_2_cv


def calculate_features(image_1, image_2, feature_number):
    
    # SIFT algorithm to find points using OpenCV library
    sift = cv2.SIFT_create(nfeatures = feature_number)

    # Keypoint array construction
    keypoints_1, descriptors_1  =  sift.detectAndCompute(image_1, None)
    keypoints_2, descriptors_2  =  sift.detectAndCompute(image_2, None)

    return keypoints_1, keypoints_2, descriptors_1, descriptors_2


def calculate_matches(descriptors_1, descriptors_2):

    brute_force = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True) #Brute force matching
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches 
    

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) -> None:

    match_img = cv2.drawMatches(
        image_1_cv,
        keypoints_1,
        image_2_cv,
        keypoints_2,
        matches[:100],
    None)

    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0) #Drawing the matches 
    cv2.destroyWindow('matches')

def calculate_mean_distance(coordinates_1: list, coordinates_2: list) -> float:
    all_distances = 0

    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference) # Pythagoras for the distance 
        all_distances = all_distances + distance

    return all_distances / len(merged_coordinates)


def calculate_speed(feature_distance, GSD: int, time_difference) -> float:
    distance = feature_distance * GSD / 100000
    speed = distance / time_difference

    return speed # RESULT FORM : KM / S

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


def main(verbose: bool = False, gsd: int = 12648) -> None:

    image_1 = 'photos/photo_07003.jpg'
    image_2 = 'photos/photo_07004.jpg'

    begin = datetime.now()
    time_difference = get_time_delta(image_1, image_2) #get time difference between images

    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) #create opencv images objects

    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(
        image_1_cv, image_2_cv,
        2000) #get keypoints and descriptors
    matches = calculate_matches(descriptors_1, descriptors_2) #match descriptors

    if verbose:
        display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) #display matches

    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)

    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    speed = calculate_speed(average_feature_distance, gsd, time_difference)

    with open('result.txt', 'w') as f:
        f.write(str(speed))


if __name__ == "__main__":
    main(verbose=False)