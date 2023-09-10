import os
import sys
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import pymongo
import plotly.express as px

from datetime import datetime

from utils import get_power_curve_pred
from models import mapper, unit_config


# Initialize database connection.
# Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_database_connection():
#     return pymongo.MongoClient("mongodb://root:pass@0.0.0.0:27017/")


# mongodb_client = init_database_connection()
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
excel_file_path = f"results_from_{formatted_datetime}.xlsx"

predictions_sample = [{
    "unit_id": "Unit1",
    "start_date": datetime(2023, 3, 1, 0),
    "stop_date": datetime(2023, 3, 1, 1),
    "prediction": "0.150"
}, {
    "unit_id": "Unit1",
    "start_date": datetime(2023, 3, 1, 1),
    "stop_date": datetime(2023, 3, 1, 2),
    "prediction": "0.105"
}, {
    "unit_id": "Unit1",
    "start_date": datetime(2023, 3, 1, 2),
    "stop_date": datetime(2023, 3, 4, 3),
    "prediction": "0.015"
}, {
    "unit_id": "Unit1",
    "start_date": datetime(2023, 3, 1, 3),
    "stop_date": datetime(2023, 3, 5, 4),
    "prediction": "0.014"
}, {
    "unit_id": "Unit1",
    "start_date": datetime(2023, 3, 1, 5),
    "stop_date": datetime(2023, 3, 1, 6),
    "prediction": "0.013"
}, {
    "unit_id": "Unit2",
    "start_date": datetime(2023, 3, 1, 2),
    "stop_date": datetime(2023, 3, 1, 3),
    "prediction": "0.012"
}]

# mongodb_client.energydb.predictions.insert_many(predictions_sample)
if 'pred_df' not in st.session_state:
    st.session_state.pred_df = None


def filter_mapper_by_interval(start_date, stop_date, mapper):
    filtered_mapper = {}

    for key, df in mapper.items():
        filtered_mapper[key] = df[(df.date_from >= start_date) & (df.date_from < stop_date)]

    return filtered_mapper

def predict_turbine(unit_list, start_date, stop_date):
    result_list = []

    start_date_time = datetime(start_date.year, start_date.month, start_date.day)
    stop_date_time = datetime(stop_date.year, stop_date.month, stop_date.day, 23, 59, 59)

    filtered_mapper = filter_mapper_by_interval(start_date_time, stop_date_time, mapper)
    pred_df = get_power_curve_pred(unit_config['power_curve_coef'], unit_config['power_curve_weights'], 
                    unit_config['unit_model_map'], filtered_mapper)
    
    pred_df['Forecast(mwh)'] = pred_df['Forecast(mwh)'].round(3)
    st.session_state.pred_df = pred_df
    print(pred_df.shape)


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

def forecast_panel(df_unit,df_weather):
    result_list=[]
    pass


def predict_sun(unit_list, start_date, stop_date):
    pass


def predict_wind(unit_list, start_date, stop_date):
    pass





def forecast(df_unit,df_weather):
    result_list=[]
    pass