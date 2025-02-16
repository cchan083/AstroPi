import pandas as pd
from datetime import datetime, timedelta

import os

from internal.speed_calc import Speed
from internal.data_logger import DataLogger
from internal.file_man import FileManager
from internal.plotter import Plotter
from internal.CONST import CONST

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
    _temperature = list(_cond["mag_x"])

    Plotter.plot_temp(
            _temperature
        )

    Plotter.plot_all([
            _cond["mag_x"],
            _cond["mag_y"],
            _cond["mag_z"]
        ])