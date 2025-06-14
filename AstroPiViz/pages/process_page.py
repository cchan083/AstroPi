import streamlit as st

#CONSTANTS

color = "white"



st.set_page_config(layout="wide")

st.title("Our Development Process")

st.markdown("""
In this project, our group will be trying to estimate the velocity of the ISS, using computer vision 

Our experiment will detect solar activity in space, using the magnetometer's readings on the sensehat 



### Dataset - used for data analysis and training
https://www.kaggle.com/datasets/arashnic/soalr-wind


## Velocity of the ISS

For our estimate of velocity calculation, we got started with the 'Finding ISS speed with photos' guide: 

https://projects.raspberrypi.org/en/projects/astropi-iss-speed/0

- However, we did change the algorithm they use to detect image features, using the SIFT algorithm, not the ORB one. 

    ```kp1, des1 = sift.detectAndCompute(image_1, None)``` - Taken from tertiary.py 

- Also, we rendered the images as grayscale as they seemed to give more accurate results (closer to 7.66) when we tested it side by side 

    ```image_1_cv = cv2.cvtColor(cv2.imread(str(image_1)), cv2.COLOR_BGR2GRAY)``` - Taken from tertiary.py 



## Building and training a model to recognise solar activity and winds 


We found out how the different components of the magnitude varied,

And what threshold was considered to be 'irregular'
""")
st.image("../photos/plot.png")

st.markdown("""Then we feature engineered the magnitude - using pythagoras' theorem

```filtered_train_a['Magnitude'] = ((filtered_train_a['bx_gse']**2) + (filtered_train_a['by_gse'] ** 2) + (filtered_train_a['bz_gse'] ** 2)) ** 0.5``` 

Then we observed how the magnitude varied as well
""")

st.image("../photos/plot1.png")

st.markdown("""
We then preprocessed the training and test data so that the magnitude of the dataset won't heavily affect classifcation of class 0 or 1, because different satallites have different magnetometer readings at different altitudes

Using standard scaler - ```scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)``` 


After that, we fixed class imbalances as very high magnitudes were rare: 

```from imblearn.under_sampling import RandomUnderSampler

under_sampler = RandomUnderSampler(sampling_strategy=1)

X_resize, y_resize = under_sampler.fit_resample(X, y)

fig, ax = plt.subplots(figsize=(5,3))
true_or_false = y_resize.value_counts().reset_index()
ax.pie(true_or_false['count'], labels=labels, colors=['turquoise', 'orange'], autopct='%1.1f%%')
ax.set_xlabel('Classes of Activity')

ax.set_title('Imbalance of data between True and False values')
``` 
""")

st.image("../photos/imbalance.png")



st.markdown("""
### Helpful links 

https://astro-pi.org/mission-space-lab 

# Test Website

https://missions.astro-pi.org/msl/replay-tool

https://www.esa.int/Education/AstroPI/Astro_PI_Sense_HAT_emulator



            """)