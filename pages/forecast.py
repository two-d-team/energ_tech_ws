import streamlit as st
import sys
import os

from prediction import forecast
from utils_dir.styles import custom_headers

st.markdown(custom_headers, unsafe_allow_html=True)


st.markdown("<h1>Forecasting</h1>", unsafe_allow_html=True)
# from prediction import predict
# st.set_page_config(
#     page_title="Form",
#     page_icon="📝"
# )
#


selected_option=st.radio('Pick one:', ['Wind Turbine','Solar Panel'])
unit_list=[]
if selected_option=="Wind Turbine":


    st.text("")
    st.subheader('Select a Unit')

    unit_1=st.checkbox('Unit1')
    if unit_1:
        unit_list.append("Unit1")
    unit_2=st.checkbox('Unit2')
    if unit_2:
        unit_list.append("Unit2")
    unit_3=st.checkbox('Unit3')
    if unit_3:
        unit_list.append("Unit3")
    unit_4=st.checkbox('Unit4')
    if unit_4:
        unit_list.append("Unit4")
    unit_5=st.checkbox('Unit5')
    if unit_5:
        unit_list.append("Unit5")
    unit_6=st.checkbox('Unit6')
    if unit_6:
        unit_list.append("Unit6")
    unit_7=st.checkbox('Unit7')
    if unit_7:
        unit_list.append("Unit7")

    st.subheader('Select number of days for forecast')

    number = st.number_input('Number of days',max_value=7,step=1)


st.button("Forecast",on_click=forecast(unit_list))







