import pandas as pd
from datetime import datetime, timedelta

import os

from internal.speed_calc import Speed
from internal.data_logger import DataLogger
from internal.file_man import FileManager
from internal.plotter import Plotter
from internal.CONST import CONST

from feature_engineering import main as predictor

import matplotlib
matplotlib.use('Agg')


"""Our team BitJam, have decided to investigate solar winds using the magnetometer on the ISS"""



if __name__ == '__main__':
    
    begin_dt = datetime.now()
    end_dt = begin_dt + timedelta(minutes=CONST.data_log_duration) # monitoring time and log duration

    FileManager.format() # creates the folders to store our data and photos
    FileManager.csv_header() # writes the headers into the csvs for data logging

    Speed.average_speed() #call average speed

    while datetime.now() < end_dt:
        DataLogger.log() 

        _cond = pd.read_csv(r"data/condition_data.csv")

        _tw = list(_cond.iloc[-3:-1])

        os.system('echo . > out.txt')
        with open("out.txt" ,"w",buffering=1) as file:
            file.write(str(_tw))

    _cond = pd.read_csv(r"data/condition_data.csv")


     # Plotting line charts 
    Plotter.plot_temp(_cond["temperature"])
    Plotter.plot_all(_cond) # magnitude
    
    
    await predictor()