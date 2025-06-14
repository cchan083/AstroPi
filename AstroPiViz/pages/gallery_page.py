import streamlit as st

st.set_page_config(layout="wide")
st.title("Gallery Page")

col1, col2 = st.columns(2, gap="large", border=True)


with col1:
    st.image("../photos/photo0-1.jpg",caption = "Photo 1")
    st.image("../photos/photo1-1.jpg",caption = "Photo 2")
    st.image("../photos/photo2-1.jpg",caption = "Photo 3")
    st.image("../photos/photo3-1.jpg",caption = "Photo 4")
    st.image("../photos/photo4-1.jpg",caption = "Photo 5")

with col2:
    st.image("../photos/photo5-1.jpg",caption = "Photo 6")
    st.image("../photos/photo6-1.jpg",caption = "Photo 7")
    st.image("../photos/photo7-1.jpg",caption = "Photo 8")
    st.image("../photos/photo8-1.jpg",caption = "Photo 9")
    st.image("../photos/photo9-1.jpg",caption = "Photo 10")