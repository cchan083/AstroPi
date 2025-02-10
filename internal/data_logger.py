from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()
sense.color.gain = 60
sense.color.integration_cycles = 64

class DataLogger:
    @staticmethod
    def get_sense_data(
            orientation=False,
            magnetometer=False,
            accelerometer=False,
            gyro=False) -> list:

        sense_data = [sense.get_temperature(), sense.get_pressure(), sense.get_humidity()]

        xyz = ["x", "y", "z"]
        ypw = ["yaw", "pitch", "roll"]

        # Get orientation data
        if orientation:
            orientation = sense.get_orientation()
            for delta in ypw:
                sense_data.append(orientation[delta])

        # Get compass data
        if magnetometer:
            mag = sense.get_compass_raw()
            for delta in xyz:
                sense_data.append(mag[delta])

        # Get accelerometer data
        if accelerometer:
            acc = sense.get_accelerometer_raw()
            for delta in xyz:
                sense_data.append(acc[delta])


        #Get gyroscope data
        if gyro:
            gyro = sense.get_gyroscope_raw()
            for delta in xyz:
                sense_data.append(gyro[delta])

        sense_data.append(datetime.now())

        return sense_data