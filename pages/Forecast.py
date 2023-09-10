from matplotlib import pyplot as plt
import streamlit as st
import sys
import os
import pandas as pd
from utils import SELECTED_FEATURES_TRAINING, get_power_curve_pred
from utils_dir.weather_api import get_forecast_weather_sun, get_forecast_weather_wind
from prediction import forecast_panel#,forecast_turbine
from models import models_dict, mapper, unit_config
import seaborn as sns
# from prediction import forecast_turbine
from utils_dir.styles import custom_headers
import plotly.express as px

if 'chart_data' not in st.session_state:
    st.session_state.chart_data = None

if 'pred_df' not in st.session_state:
    st.session_state.pred_df = None

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


def forecast_turbine(unit_list, nr_of_days):
    print('inside forecast turbine... \n\n')
    df_units, weather_df = get_forecast_weather_wind(nr_of_days, unit_list)

    merged_df = df_units.merge(weather_df, left_on=['latitude', 'longitude'], right_on=['latitude', 'longitude'])

    groups = merged_df.groupby('wind_plant')

    local_mapper = {}
    for unit_name, df in groups:
        print(df.columns)
        local_mapper[unit_name] = df


    pred_df = get_power_curve_pred(unit_config['power_curve_coef'], unit_config['power_curve_weights'], 
                                unit_config['unit_model_map'], local_mapper)


    print(pred_df)
    # Creating the plot
    fig = px.line(pred_df, x='date_from', y='Forecast(mwh)', color='wind_plant', title='Wind Plant Forecast')
    st.session_state.chart_data = fig

    pred_df['Forecast(mwh)'] = pred_df['Forecast(mwh)'].round(3)
    st.session_state.pred_df = pred_df

    # plt.figure(figsize=(14, 7))
    # sns.lineplot(x='date_from', y='Forecast(mwh)', hue='wind_plant', data=pred_df)
    # plt.title('Wind Plant Forecast')
    # plt.xlabel('Time')
    # plt.ylabel('Forecast (mwh)')
    # plt.xticks(rotation=45)

    # Display in Streamlit
    pred_df.to_excel("pred_df.xlsx")
    # merged_df['date'] = merged_df.date_time_from.dt.date
    # merged_df['date'] = merged_df.date_time_from.dt.date
    # merged_df['date_tp'] = merged_df.date_time_from.copy()

    # groups = merged_df.groupby('wind_plant')

    # for unit_name, df in groups:
    #     cols = ['wind_speed (m/s)', 'wind_dir', 'temp', 'pressure', 'Tower Height',
    #    'Rotor Diameter', 'date_from', 'date_to', 'month',
    #    'hour', 'day']
        
    #     pred = models_dict[unit_name].predict(df[cols])
    #     print(pred)


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

    #forecast_bt=st.button("Forecast",on_click=get_forecast_weather(number_days,coordinates))
    forecast_bt = st.button("Forecast", on_click=lambda: forecast_turbine(unit_list, number_days))
    if st.session_state.pred_df is not None:
        csv = st.session_state.pred_df.to_csv(index=False)
        st.download_button(
            label="Download Forecast Data",
            data=csv,
            file_name="forecast_data.csv",
            mime="text/csv",
        )
    if st.session_state.chart_data is not None:
        st.plotly_chart(st.session_state.chart_data)
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









