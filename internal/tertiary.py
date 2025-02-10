import cv2
import math
from datetime import datetime
from exif import Image

class Tertiary:
    @staticmethod
    def get_time(path: str) -> datetime:
        """Extracts the original datetime from an image's EXIF metadata."""
        with open(path, 'rb') as image_file:
            img = Image(image_file)
            time_str = img.get("datetime_original")
            return datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')

    @staticmethod
    def get_time_delta(image_path_1: str, image_path_2: str) -> float:
        """Calculates the time difference (in seconds) between two images."""
        time_1 = Tertiary.get_time(image_path_1)
        time_2 = Tertiary.get_time(image_path_2)
        return (time_2 - time_1).total_seconds()

    @staticmethod
    def convert_to_cv(image_1: str, image_2: str):
        """Converts images to grayscale OpenCV format."""
        image_1_cv = cv2.cvtColor(cv2.imread(image_1), cv2.COLOR_BGR2GRAY)
        image_2_cv = cv2.cvtColor(cv2.imread(image_2), cv2.COLOR_BGR2GRAY)
        return image_1_cv, image_2_cv

    @staticmethod
    def calculate_features(image_1, image_2, feature_number: int):
        """Detects SIFT features in two images."""
        sift = cv2.SIFT_create(nfeatures=feature_number)
        kp1, des1 = sift.detectAndCompute(image_1, None)
        kp2, des2 = sift.detectAndCompute(image_2, None)
        return kp1, kp2, des1, des2

    @staticmethod
    def calculate_matches(des1, des2):
        """Finds feature matches between two images using BFMatcher."""
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(des1, des2)
        return sorted(matches, key=lambda x: x.distance)

    @staticmethod
    def find_matching_coordinates(kp1, kp2, matches):
        """Extracts matched keypoints' coordinates."""
        coords1 = [kp1[m.queryIdx].pt for m in matches]
        coords2 = [kp2[m.trainIdx].pt for m in matches]
        return coords1, coords2

    @staticmethod
    def calculate_mean_distance(coords1, coords2):
        """Computes the average distance between matched keypoints."""
        total_distance = sum(math.hypot(x2 - x1, y2 - y1) for (x1, y1), (x2, y2) in zip(coords1, coords2))
        return total_distance / len(coords1) if coords1 else 0

    @staticmethod
    def calculate_speed(mean_dist: float, gsd: float, time_delta: float) -> float:
        """Calculates object speed in km/s given ground sample distance (GSD) and time delta."""
        if time_delta == 0:
            return 0
        distance_km = (mean_dist * gsd) / 100000  # Convert cm to km
        return distance_km / time_delta  # km/s

