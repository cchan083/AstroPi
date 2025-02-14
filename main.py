from datetime import datetime, timedelta

from internal.speed_calc import Speed
from internal.data_logger import DataLogger
from internal.file_man import FileManager
from internal.CONST import CONST

# TODO
# Possibly look at threading the data collection


if __name__ == '__main__':
    begin_dt = datetime.now()
    end_dt = begin_dt + timedelta(minutes=CONST.data_log_duration)

    FileManager.format()
    FileManager.csv_header()

    Speed.average_speed()

    while datetime.now() < end_dt:
        DataLogger.log()