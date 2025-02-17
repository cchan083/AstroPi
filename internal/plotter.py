import matplotlib
matplotlib.use('Agg')  # or 'TkAgg' if you have a GUI environment
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

class Plotter:
    @staticmethod
    def plot_temp(data: list) -> None:
        plt.plot(data)
        plt.savefig('temperature.png')
        plt.close()

    @staticmethod
    def plot_all(data) -> None:
        #data = dataframe.to_numpy()
        data['mag_hypotenuse'] = ((data['mag_x'] ** 2) + (data['mag_y'] ** 2) + (data['mag_z'] ** 2))**0.5

        # Convert the 'datetime' column to a proper datetime format
        data['datetime'] = pd.to_datetime(data['datetime'], format='%M:%S.%f')

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(data['datetime'], data['mag_hypotenuse'], marker='o', linestyle='-', color='b')

        # Add labels and title
        plt.xlabel('Time')
        plt.ylabel('Magnetic Hypotenuse')
        plt.title('Magnetic Hypotenuse Over Time')
        plt.grid(True)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Show the plot
        plt.tight_layout()
        plt.savefig('hypotenuse.png')
        plt.close()