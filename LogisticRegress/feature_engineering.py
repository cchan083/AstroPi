import pandas as pd
import pickle
import micropip


# Synchronously install scikit-learn using micropip
def install_sklearn():
    micropip.install("scikit-learn")  # Install synchronously
    from sklearn.preprocessing import StandardScaler
    return StandardScaler

# TODO
# Closer, still horrible stuff


# Install scikit-learn and get StandardScaler
StandardScaler = install_sklearn()


def add_features():
    df = pd.read_csv('LogisticRegress/results.csv')

    df = df.drop([
        'temp',
        'pres',
        'hum',
        'red',
        'green',
        'blue',
        'clear',
        'yaw',
        'pitch',
        'roll',
        'acc_x',
        'acc_y',
        'acc_z',
        'gyro_x',
        'gyro_y',
        'gyro_z',
        'datetime'
    ], axis=1)

    df = df.rename(columns={'mag_x': 'filtered_x', 'mag_y': 'by_gse', 'mag_z': 'bz_gse'})
    df['minutes'] = df.index
    df['Magnitude'] = ((df['filtered_x'] ** 2) + (df['by_gse'] ** 2) + (df['bz_gse'] ** 2)) ** 0.5
    X = df[['filtered_x', 'Magnitude', 'minutes', 'by_gse', 'bz_gse']]
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    return scaled_X


def model_predict():
    with open('LogisticRegress/model.csv', 'rb') as f:
        model = pickle.load(f)
    y_pred = model.predict(add_features())

    print(f'predicted values: {y_pred}')
    new_df = pd.read_csv('results.csv')
    new_df['predictions'] = y_pred
    with open('predictions.csv', 'wb') as f:
        pickle.dump(new_df, f)


if __name__ == '__main__':
    model_predict()