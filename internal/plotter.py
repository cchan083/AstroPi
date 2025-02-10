import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd

class Plotter:
    @staticmethod
    def plot_line(data_name, feature, title, xlabel, ylabel, file_name):
        df = pd.read_csv(data_name)
        df['time'] = [x * 30 for x in range(len(df))]
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(df['time'], df[feature], color='salmon')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis='x', labelsize=5)
        plt.savefig(file_name)