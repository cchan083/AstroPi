import matplotlib as plt
import pandas as pd


# condition_data.csv
# df.head() ==
"""pressure	temperature	humidity
993.3807631	34.18958671	29.75153882
993.3824348	33.81263602	29.51346928
993.361825	33.8482893	29.73591217
993.3444468	33.97258488	29.12044916
993.3893762	33.85532038	31.31571314"""


def plot_line(data_name, feature, title, xlabel, ylabel, file_name):
    df = pd.read_csv(data_name)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df['datetime'], df[feature], color='salmon')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(file_name)