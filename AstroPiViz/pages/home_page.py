import streamlit as st
from pathlib import Path

def home():
    st.title("AstroPi - BitJam Project summary and Data Visualisation")
    image_path = Path(__file__).parent.parent / "photos" / "photo4-1.jpg"
    st.image(str(image_path), caption="One of the photos we took from the ISS")

home()