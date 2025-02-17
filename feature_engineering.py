import pandas as pd

import pickle
import asyncio
import micropip

# Define an async function to install the package
async def install_package():
 
    await micropip.install('scikit-learn')
    from sklearn.preprocessing import StandardScaler
#Feature engineering the magnitude
asyncio.run(install_package())

from sklearn.preprocessing import StandardScaler

def add_features():
    df = pd.read_csv('results.csv')

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
    
    df = df.rename(columns={'mag_x':'filtered_x', 'mag_y':'by_gse', 'mag_z':'bz_gse'})
    df['minutes'] = df.index
    df['Magnitude'] = ((df['filtered_x']**2) + (df['by_gse'] ** 2) + (df['bz_gse'] ** 2)) ** 0.5
    X = df[['filtered_x', 'Magnitude','minutes', 'by_gse', 'bz_gse']]
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    return scaled_X

def model_predict():
    with open('model.csv', 'rb') as f:
        model = pickle.load(f)
    y_pred = (model.predict_proba(add_features())[:,1] >= 0.9).astype(int)
    
    
    new_df = pd.read_csv('data//condition_data.csv')
    new_df['predictions'] = y_pred
    

model_predict()
    

