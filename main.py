from threaded_calc import main as avg_threaded
from unthreaded_calc import average_speed as avg_unthreaded
from data_logger import get_sense_data as log_data

from datetime import datetime as dt
from datetime import timedelta

import time

begin = dt.now()
stringify = lambda x : [str(i) for i in x]

if __name__ == '__main__':
    try:
        avg_threaded(verbose=False)
    except RuntimeError as e:
        print(e)
        avg_unthreaded()


    while dt.now() < begin + timedelta(minutes=3):
        data = log_data()
        strung = stringify(data)

        with open("results.csv", "w") as f:
            f.write(','.join(['temp', 'pres', 'hum',
                              'red', 'green', 'blue', 'clear',
                              'yaw', 'pitch', 'roll',
                              'mag_x', 'mag_y', 'mag_z',
                              'acc_x', 'acc_y', 'acc_z',
                              'gyro_x', 'gyro_y', 'gyro_z',
                              'datetime']))

        with open("results.csv", "a") as f:
            f.write('\n' + ','.join(strung))

        time.sleep(1)