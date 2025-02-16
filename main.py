import pandas as pd
from datetime import datetime, timedelta

import os

from internal.speed_calc import Speed
from internal.data_logger import DataLogger
from internal.file_man import FileManager
from internal.plotter import Plotter
from internal.CONST import CONST

from LogisticRegress.feature_engineering import model_predict

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import numpy as np

if __name__ == '__main__':
    begin_dt = datetime.now()
    end_dt = begin_dt + timedelta(minutes=CONST.data_log_duration)

    FileManager.format()
    FileManager.csv_header()

    Speed.average_speed()

    while datetime.now() < end_dt:
        DataLogger.log()

        _cond = pd.read_csv(r"data\condition_data.csv")

        _tw = list(_cond.iloc[-3:-1])

        os.system('echo . > out.txt')
        with open("out.txt" ,"w") as file:
            file.write(str(_tw))

    model_predict()

    Plotter.plot_temp(_cond["temperature"])
    Plotter.plot_all(_cond)
        