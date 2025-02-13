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
                os.mkdir(folder)