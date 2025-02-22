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

if __name__ == '__main__':
    
    begin_dt = datetime.now()
    end_dt = begin_dt + timedelta(minutes=CONST.data_log_duration) # monitoring time and log duration

    FileManager.format()
    FileManager.csv_header()

    Speed.average_speed() #call average speed

    while datetime.now() < end_dt:
        DataLogger.log()

        _cond = pd.read_csv(r"data/condition_data.csv")

        _tw = list(_cond.iloc[-3:-1])

        os.system('echo . > out.txt')
        with open("out.txt" ,"w") as file:
            file.write(str(_tw))

    _cond = pd.read_csv(r"data/condition_data.csv")

    Plotter.plot_temp(_cond["temperature"])
    Plotter.plot_all(_cond)
    
    
    await predictor()