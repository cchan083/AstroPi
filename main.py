from threaded_calc import main as avg_threaded

from unthreaded_calc import average_speed as avg_unthreaded

from data_logger import get_humidity_temperature_pressure as temp_data
from data_logger import get_sense_data as log_data

from plotter import plot_line

from datetime import datetime as dt
from datetime import timedelta
import numpy as np
from matplotlib import pyplot as plt
import time

begin = dt.now()
stringify = lambda x : [str(i) for i in x]

if __name__ == '__main__':
    try:
        avg_threaded(verbose=False)
    except RuntimeError as e:
        print(e)
        avg_unthreaded()

    with open("results.csv", "w") as f:
        f.write(','.join(['temp', 'pres', 'hum',
                          'red', 'green', 'blue', 'clear',
                          'yaw', 'pitch', 'roll',
                          'mag_x', 'mag_y', 'mag_z',
                          'acc_x', 'acc_y', 'acc_z',
                          'gyro_x', 'gyro_y', 'gyro_z',
                          'datetime']))
    
    with open('condition_data.csv', 'a') as f:
        f.write(','.join(['pressure', 'temperature', 'humidity', 'datetime']))

    new_time = dt.now() + timedelta(minutes=3)
    while dt.now() < new_time:
        data = log_data()
        strung = stringify(data)
        condition_data = temp_data()
        temp_strung = stringify(condition_data)
        

        with open("results.csv", "a") as f:
            f.write('\n' + ','.join(strung))
        
        with open('condition_data.csv','a') as f:
            f.write('\n' + ','.join(temp_strung))
    
    

        time.sleep(1)
        


    plot_line('condition_data.csv', 'temperature', 'temperature change over time', 'time', 'temperature in celcius', 'plot.png')
"""
    with open("results.csv", "r") as f:
        content = np.rot90([i.strip().split(",") for i in f.readlines()][1:])

    for axis in content:
        Y = axis
        X = np.arange(1, len(axis))
        plt.plot(X,Y)

    plt.savefig("plot.png")"""
    
