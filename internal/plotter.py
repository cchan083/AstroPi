import matplotlib
matplotlib.use('Agg')  # or 'TkAgg' if you have a GUI environment
import matplotlib.pyplot as plt

class Plotter:
    @staticmethod
    def plot_temp(data: list) -> None:
        plt.plot(data)
        plt.savefig('temperature.png')
        plt.close()

    @staticmethod
    def plot_all(dataframe: list) -> None:
        for data in dataframe:
            plt.plot(data)
        plt.savefig('all.png')
        plt.close()
