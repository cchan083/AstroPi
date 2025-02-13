from datetime import datetime, timedelta
import time

from internal.speed_calc import Speed
from internal.data_logger import DataLogger
from internal.file_man import FileManager

from internal.CONST import CONST

# from internal.plotter import Plotter

FileManager.format()

begin = datetime.now()
stringify = lambda x : [str(i) if i else "" for i in x]

# TODO
# Fix the photos bugging out in the photos folder.
# Implement timing controls
# Possibly look at threading the data collection


if __name__ == '__main__':
    Speed.average_speed()

    with open("data\\results.csv", "w") as f:
        f.write(','.join(['temp', 'pres', 'hum',
                          'yaw', 'pitch', 'roll',
                          'mag_x', 'mag_y', 'mag_z',
                          'acc_x', 'acc_y', 'acc_z',
                          'gyro_x', 'gyro_y', 'gyro_z',
                          'datetime']))

    with open('data\\condition_data.csv', 'a') as f:
        f.write(','.join(['temperature',
                          'pressure',
                          'humidity',
                          'datetime']))


    upper_bound = datetime.now() + timedelta(minutes=CONST.data_log_duration)
    while datetime.now() < upper_bound:
        data = DataLogger.get_sense_data(
            orientation   = True,
            magnetometer  = True,
            accelerometer = True,
            gyro          = True,
        )
        strung = stringify(data)

        condition_data = DataLogger.get_sense_data(

            orientation   = False,
            magnetometer  = False,
            accelerometer = False,
            gyro          = False,
        )
        temp_strung = stringify(condition_data)


        with open("data\\results.csv", "a") as f:
            f.write('\n' + ','.join(strung))

        with open('data\\condition_data.csv','a') as f:
            f.write('\n' + ','.join(temp_strung))


        time.sleep(
            CONST.data_log_interval
        )