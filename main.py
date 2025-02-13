from datetime import datetime, timedelta
import time

from internal.speed_calc import Speed
from internal.data_logger import DataLogger
# from internal.plotter import Plotter

begin = datetime.now()
stringify = lambda x : [str(i) for i in x]

if __name__ == '__main__':
    Speed.average_speed()

    with open("results.csv", "w") as f:
        f.write(','.join(['temp', 'pres', 'hum',
                          'yaw', 'pitch', 'roll',
                          'mag_x', 'mag_y', 'mag_z',
                          'acc_x', 'acc_y', 'acc_z',
                          'gyro_x', 'gyro_y', 'gyro_z',
                          'datetime']))

    with open('condition_data.csv', 'a') as f:
        f.write(','.join(['temperature',
                          'pressure',
                          'humidity',
                          'datetime']))


    upper_bound = datetime.now() + timedelta(minutes=1)
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


        with open("results.csv", "a") as f:
            f.write('\n' + ','.join(strung))

        with open('condition_data.csv','a') as f:
            f.write('\n' + ','.join(temp_strung))


        time.sleep(30)

    # Plotter.plot_line('condition_data.csv',
    #           'temperature',
    #           'temperature change over time',
    #           'time', 'temperature in celsius',
    #           'plot.png')
    #
    #
