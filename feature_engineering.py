
import pickle
import pandas as pd

import micropip
#await micropip.install('scikit-learn')
# Sklearn doesn't work so standard scaler manually with np
import asyncio
import numpy as np

def StandardScaler(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    return (data - mean) / std



async def model_predict():
    await micropip.install('scikit-learn')
    print('sklearn installed')
    
    df = pd.read_csv('data/results.csv')
    
    df = pd.read_csv('data/results.csv')
    df = df.drop([
        'temp',
        'pres',
        'hum',
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
    
    df = df.rename(columns={'mag_x':'filtered_x', 'mag_y':'by_gse', 'mag_z':'bz_gse'})
    df['minutes'] = df.index / 2
    df['Magnitude'] = ((df['filtered_x']**2) + (df['by_gse'] ** 2) + (df['bz_gse'] ** 2)) ** 0.5
    X = df[['filtered_x', 'Magnitude','minutes', 'by_gse', 'bz_gse']]
    scaled_X = StandardScaler(X)
    scaled_X = scaled_X.to_numpy()
    
    from sklearn.linear_model import LogisticRegression
    
    with open('model.csv', 'rb') as f:
        model = pickle.load(f)
        
    y_pred = (model.predict_proba((scaled_X))[:,1] >= 0.9).astype(int)
    df['predictions'] = y_pred
    std_dev = df['Magnitude'].std()
    mean_val = df['Magnitude'].mean()


    if (std_dev < 5) and (30 <= mean_val <= 45):
        df['Threshold_Column'] = 0
    else:
        df['Threshold_Column'] = df['raw_predicitions']
    
    df.to_csv('results.csv', index=False)
    

async def main():
    await model_predict()



