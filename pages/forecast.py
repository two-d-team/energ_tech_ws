import streamlit as st
import sys
import os
import pandas as pd
from utils_dir.weather_api import get_forecast_weather_sun, get_forecast_weather_wind
from prediction import forecast_panel,forecast_turbine


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(parent_dir)
sys.path.append(parent_dir+"/utils")

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
new_unit_list=[]
weather_df=None


def checkbox_container(data):
    cols = st.columns(5)
    if cols[0].button('Select All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
        st.experimental_rerun()
    if cols[1].button('UnSelect All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
        st.experimental_rerun()
    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i)

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_', '') for i in st.session_state.keys() if
            i.startswith('dynamic_checkbox_') and st.session_state[i]]

if selected_option=="Wind Turbine":


    st.text("")
    st.subheader('Select a Unit')

    import streamlit as st

    if 'dummy_data' not in st.session_state.keys():
        dummy_data = ['Unit1', 'Unit2', 'Unit3', 'Unit4', 'Unit5','Unit6','Unit7']
        st.session_state['dummy_data'] = dummy_data
    else:
        dummy_data = st.session_state['dummy_data']

    checkbox_container(dummy_data)
    st.write('You selected:')
    unit_list=get_selected_checkboxes()


    st.subheader('Select number of days for forecast')

    number_days = st.number_input('Number of days',max_value=7,step=1)

    coordinates = "47.034746,28.421021"


    #forecast_bt=st.button("Forecast",on_click=get_forecast_weather(number_days,coordinates))
    forecast_bt = st.button("Forecast", on_click=forecast_turbine(get_forecast_weather_wind(number_days,unit_list)[0],get_forecast_weather_wind(number_days,unit_list)[1]))

elif selected_option=="Solar Panel":

    if 'sun_data' not in st.session_state.keys():
        sun_data = ['Unit1']
        st.session_state['sun_data'] = sun_data
    else:
        sun_data = st.session_state['sun_data']

    checkbox_container(sun_data)
    st.write('You selected:')
    unit_list = get_selected_checkboxes()

    st.subheader('Select number of days for forecast')

    number_days = st.number_input('Number of days', max_value=7, step=1)

    forecast_bt = st.button("Forecast",on_click=forecast_panel(get_forecast_weather_sun(number_days,unit_list)[0],get_forecast_weather_sun(number_days,unit_list)[1]))









