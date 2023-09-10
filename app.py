import streamlit as st

from utils_dir import styles
from utils_dir.texts import text

st.set_page_config(
    page_title="Green Energy Production Forecasting",
    page_icon="🔋",
)

st.markdown(styles.custom_headers, unsafe_allow_html=True)

st.markdown("<h1>EnergyForecast AI</h1>", unsafe_allow_html=True)

#st.markdown("<h1 style='text-align: center; color: #00e905; white-space: nowrap;'>Green EnergyTech</h1>", unsafe_allow_html=True)
st.markdown("<h2>Powering the Future 🌍🌿</h2>", unsafe_allow_html=True)

st.image("images/stable-diffusion-xl.jpg")
#Green Energy Production Forecasting: Powering the Future 🌍🌿
st.header('About The Project')

#st.text(body=texts.text)
st.markdown(text, unsafe_allow_html=True)

st.caption('Balloons. Hundreds of them...')





