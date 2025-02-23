import os

class FileManager:
    @staticmethod
    def format():
        dirs = os.listdir()

        folders = [
            "photos",
            "data"
        ]

        for folder in folders:
            if folder not in list(dirs):
                os.mkdir(folder) #make photos and the data folder 
            

    @staticmethod
    def csv_header():
    
        with open("data/results.csv", "a") as f:
            f.write(','.join(['temp', 'pres', 'hum',
                              'yaw', 'pitch', 'roll',
                              'mag_x', 'mag_y', 'mag_z',
                              'acc_x', 'acc_y', 'acc_z',
                              'gyro_x', 'gyro_y', 'gyro_z',
                              'datetime']))

        with open('data/condition_data.csv', 'a') as f:
            f.write(','.join(['temperature',
                              'pressure',
                              'humidity',
                              'mag_x', 'mag_y', 'mag_z',
                              'datetime']))