from exif import Image
from datetime import datetime
import threading
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

def get_time(path: str = "") -> datetime:
    with open(path, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')  # Extract timestamp

    return time

def time_delta(img_1: str = None, img_2: str = None) -> float:
    workers = [
        Worker(get_time, 1, img_1),
        Worker(get_time, 2, img_2)
    ]

    for worker in workers:
        worker.start()  # Start all threads

    for worker in workers:
        worker.join()  # Wait for all threads

    results = {worker.identifier: worker.result for worker in workers}
    delta = results[2] - results[1]

    return delta.total_seconds()  # cast time delta to seconds

def main(verbose=False) -> None:
    if verbose:
        begin = datetime.now()

    image_1 = 'photos/photo_07003.jpg'
    image_2 = 'photos/photo_07004.jpg'

    delta = time_delta(image_1, image_2)

    print(delta)
    if verbose:
        print(f"Time Elapsed: {datetime.now() - begin}")

if __name__ == "__main__":
    main(verbose=True)
