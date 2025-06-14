import streamlit as st
import pandas as pd
from pathlib import Path


st.set_page_config(layout="wide")
st.title("Graphs and Plots")


graph_tab, predictions_tab= st.tabs([
        "📊 Graphs and Plots", 
        "Predictions",
    ])

results_path = Path(__file__).parent.parent / "csvs" / "results.csv"
condition_path = Path(__file__).parent.parent / "csvs" / "condition_data.csv"

predictions = pd.read_csv(str(results_path))
condition_data = pd.read_csv(str(condition_path))
condition_data['datetime'] = condition_data['datetime'].str[11:16]
  

with graph_tab:
    col1, col2 = st.columns(2, gap='medium', border=True)
    with col1:
        
        st.subheader("Humidity Data")
        st.line_chart(condition_data,
                x='datetime',
                y='humidity',
                x_label='Time (Hrs/mins)',
                y_label='Humidity',
                )
        
        st.subheader("Temperature Data")
        st.line_chart(condition_data,
                x='datetime',
                y='temperature',
                x_label='Time (Hrs/mins)',
                y_label='Temperature (c)',
                )

    with col2:
        
        st.subheader("Magnitude of Magentometer Readings")
        st.line_chart(predictions,
                x='minutes',
                y='Magnitude',
                x_label='Time (mins)',
                y_label='Magnitude',
                )
        
        st.subheader("Pressure Data")
        st.line_chart(condition_data,
                x='datetime',
                y='pressure',
                x_label='Time (Hrs/mins)',
                y_label='pressure',
                ) 
    

with predictions_tab:
    col1, col2 = st.columns([6.5, 3.5], border=True)
    
    with col1:
        st.subheader("3 Axis' of Magnetometer Readings")
        
        st.line_chart(predictions,
                      x='minutes',
                      y=['filtered_x', 'by_gse', 'bz_gse'],
                      x_label='Time (mins)',
                      y_label="Magnetometer Readings")
        
        st.subheader("Magnitude of Magentometer Readings")
        st.line_chart(predictions,
                x='minutes',
                y='Magnitude',
                x_label='Time (mins)',
                y_label='Magnitude',
        )
    
    with col2:

        st.table(predictions)
        
        st.subheader("Predictions of sudden solar activity")
        st.line_chart(predictions,
                      x='minutes',
                      y=['raw_predictions'],
                      x_label='Time (mins)',
                      y_label='Binary Predictions (1 or 0)')