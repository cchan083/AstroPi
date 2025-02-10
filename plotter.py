import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd


def plot_line(data_name, feature, title, xlabel, ylabel, file_name):
    df = pd.read_csv(data_name)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df['datetime'], df[feature], color='salmon')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.xticks(fontsize=5, rotation=45)
    plt.savefig(file_name)