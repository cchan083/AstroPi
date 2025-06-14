import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")
st.title("Gallery Page")

col1, col2 = st.columns(2, gap="large", border=True)




with col1:
    image_path_1 = Path(__file__).parent.parent / "photos" / "photo0-1.jpg"
    st.image(str(image_path_1),caption = "Photo 1")
    
    image_path_2 = Path(__file__).parent.parent / "photos" / "photo1-1.jpg"
    st.image(str(image_path_2),caption = "Photo 2")
    
    image_path3 = Path(__file__).parent.parent / "photos" / "photo2-1.jpg"
    st.image(str(image_path3),caption = "Photo 3")
    
    image_path4 = Path(__file__).parent.parent / "photos" / "photo3-1.jpg"
    st.image(str(image_path4),caption = "Photo 4")
    
    image_path5 = Path(__file__).parent.parent / "photos" / "photo4-1.jpg"
    st.image(str(image_path5),caption = "Photo 5")

with col2:
    image_path6 = Path(__file__).parent.parent / "photos" / "photo5-1.jpg"
    st.image(str(image_path6),caption = "Photo 6")
    
    image_path7 = Path(__file__).parent.parent / "photos" / "photo6-1.jpg"
    st.image(str(image_path7),caption = "Photo 7")
    
    image_path8 = Path(__file__).parent.parent / "photos" / "photo7-1.jpg"
    st.image(str(image_path8),caption = "Photo 8")
    
    image_path9 = Path(__file__).parent.parent / "photos" / "photo8-1.jpg"
    st.image(image_path9,caption = "Photo 9")
    
    image_path10 = Path(__file__).parent.parent / "photos" / "photo9-1.jpg"
    st.image(image_path10,caption = "Photo 10")