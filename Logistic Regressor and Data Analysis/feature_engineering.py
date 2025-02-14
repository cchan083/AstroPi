import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
#Feature engineering the magnitude

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
    
    df['Magnitude'] = ((df['filtered_x']**2) + (df['by_gse'] ** 2) + (df['bz_gse'] ** 2)) ** 0.5
    X = df[['filtered_x', 'Magnitude', 'by_gse', 'bz_gse']]
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    return scaled_X

def model_predict():
    with open('model.csv', 'rb') as f:
        model = joblib.load(f)
    y_pred = model.predict(add_features())
    print(f'predicted values: {y_pred}')
    

model_predict()
    

