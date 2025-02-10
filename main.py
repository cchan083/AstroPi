from speed_calc import average_speed as avg_speed
from data_logger import DataLogger

from plotter import plot_line

from datetime import datetime
from datetime import timedelta

import numpy as np
from matplotlib import pyplot as plt

import time
begin = datetime.now()

stringify = lambda x : [str(i) for i in x]

if __name__ == '__main__':
    avg_speed()

    with open("results.csv", "w") as f:
        f.write(','.join(['temp', 'pres', 'hum',
                          'yaw', 'pitch', 'roll',
                          'mag_x', 'mag_y', 'mag_z',
                          'acc_x', 'acc_y', 'acc_z',
                          'gyro_x', 'gyro_y', 'gyro_z',
                          'datetime']))
    
    with open('condition_data.csv', 'a') as f:

        f.write(','.join(['pressure',
                          'temperature',
                          'humidity',
                          'datetime']))

    new_time = datetime.now() + timedelta(minutes=8)
    while datetime.now() < new_time:
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
        

        with open("results.csv", "a") as f:
            f.write('\n' + ','.join(strung))
        
        with open('condition_data.csv','a') as f:
            f.write('\n' + ','.join(temp_strung))


        time.sleep(30)
        


    plot_line('condition_data.csv',
              'temperature',
              'temperature change over time',
              'time', 'temperature in celcius',
              'plot.png')


