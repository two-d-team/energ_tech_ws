import streamlit as st
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(parent_dir)

from utils_dir.styles import custom_headers


st.markdown(custom_headers, unsafe_allow_html=True)


st.markdown("<h1>Data Insights</h1>", unsafe_allow_html=True)

#st.markdown("<h1 style='text-align: center; color: #00e905; white-space: nowrap;'>Green EnergyTech</h1>", unsafe_allow_html=True)
st.markdown("<h2>location of wind turbines</h2>", unsafe_allow_html=True)
st.markdown("<h3>data plot 1 </h3>", unsafe_allow_html=True)
#st.image()
st.caption('caption for image')

#Green Energy Production Forecasting: Powering the Future 🌍🌿
st.header('My header')

st.subheader('My sub')

st.text('Fixed width text')

st.caption('Balloons. Hundreds of them...')





