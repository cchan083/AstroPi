

import pandas as pd
import numpy as np

import json



# This file loads in the logistic regression model we trained ourselves, using the model_params.json

# our data analysis and model training found here https://github.com/cchan083/AstroPi

# reconstruct the model here

def StandardScaler(data):
    mean = np.mean(data, axis=0) 
    std = np.std(data, axis=0)
    return (data - mean) / std
    # data normalised so that model is not reliant on magnitude 

 


def model_predict():
    try:
        from sklearn.linear_model import LogisticRegression
        # Hope that sklearn is installed as the replay tool does not have it installed
    except:    
        print('Sklearn is not there')

    
    df = pd.read_csv('results.csv')
    
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
    
    #drop unnecessary columns
    
    df = df.rename(columns={'mag_x':'filtered_x', 'mag_y':'by_gse', 'mag_z':'bz_gse'})
    df['minutes'] = df.index / 2 
    # feature engineer the time interval 
    
    df['Magnitude'] = ((df['filtered_x']**2) + (df['by_gse'] ** 2) + (df['bz_gse'] ** 2)) ** 0.5
    # Feature engineer the overall magnitude of all 3 axes 
    
    X = df[['filtered_x', 'Magnitude','minutes', 'by_gse', 'bz_gse']]
    scaled_X = StandardScaler(X) #normalise data
    scaled_X = scaled_X.to_numpy() 
    
    
    
    with open("model_params.json", "r") as f:
        params = json.load(f) #load parameters and model_weights

    try:
        model = LogisticRegression()
        
        X_dummy = np.array([ 
        [0, 1, 2, 3, 4],  
        [1, 2, 3, 4, 5]   
    ])


        y_dummy = np.array([0, 1])  # Dummy input and output to init model
            
        model.fit(X_dummy, y_dummy)
        
        model.coef_ = np.array(params["coef"])  # Convert back to NumPy array
        model.intercept_ = params["intercept"]
        
        y_pred = (model.predict_proba((scaled_X))[:,1] >= 0.9).astype(int) 

        # reject probabilities under 0.9 for class 1 
        df['raw_predictions'] = y_pred
        std_dev = df['Magnitude'].std()
        mean_val = df['Magnitude'].mean()


        if (std_dev < 5) and (30 <= mean_val <= 45):
            # between 30 and 45 is considered 'normal'
            df['Threshold_Column'] = 0
        else:
            df['Threshold_Column'] = y_pred
        
        df.to_csv('results.csv', index=False)
    except:
        print('sklearn not installed')
    





