from sense_hat import SenseHat
from datetime import datetime
import time

from internal.CONST import CONST

sense = SenseHat()

class DataLogger:
    @staticmethod
    def get_sense_data(
            orientation=False,
            magnetometer=False,
            accelerometer=False,
            gyro=False) -> dict:
        """returns toggleable sensor data inside an array"""

        sense_data = {
            "temp" : sense.get_temperature(),
            "pres" : sense.get_pressure(),
            "humid": sense.get_humidity()
                      }

        # TODO
        # Change this to a dictionary

        xyz = ["x", "y", "z"]
        ypw = ["yaw", "pitch", "roll"]

        # Get orientation data
        if orientation:
            orientation = sense.get_orientation()
            for delta in ypw:
                sense_data[f"{delta}"]  = (orientation[delta])

        # Get compass data
        if magnetometer:
            mag = sense.get_compass_raw()
            for delta in xyz:
                sense_data[f"mag_{delta}"] = (mag[delta])

        # Get accelerometer data
        if accelerometer:
            acc = sense.get_accelerometer_raw()
            for delta in xyz:
                sense_data[f"acc_{delta}"] = (acc[delta])


        #Get gyroscope data
        if gyro:
            gyro = sense.get_gyroscope_raw()
            for delta in xyz:
                sense_data[f"gyro_{delta}"] = (gyro[delta])

        sense_data[f"datetime"] = (datetime.now())

        return sense_data

    @staticmethod
    def log():
        stringify = lambda x: [str(i) if i else "" for i in x]

        data = DataLogger.get_sense_data(
            orientation=True,
            magnetometer=True,
            accelerometer=True,
            gyro=True,
        )
        strung = stringify(data.values())

        condition_data = DataLogger.get_sense_data(
            orientation=False,
            magnetometer=False,
            accelerometer=False,
            gyro=False,
        )
        temp_strung = stringify(condition_data.values())

        with open("data\\results.csv", "a") as f:
            f.write('\n' + ','.join(strung))

        with open('data\\condition_data.csv', 'a') as f:
            f.write('\n' + ','.join(temp_strung))

        time.sleep(
            CONST.data_log_interval
        )