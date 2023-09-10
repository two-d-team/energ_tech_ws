import os
import sys
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import pymongo
import plotly.express as px

from datetime import datetime


# Initialize database connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_database_connection():
    return pymongo.MongoClient("mongodb://root:pass@0.0.0.0:27017/")


mongodb_client = init_database_connection()
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


def forecast_turbine(unit_list, start_date, stop_date):
    result_list = []
    start_date_time = datetime(start_date.year, start_date.month, start_date.day)
    stop_date_time = datetime(stop_date.year, stop_date.month, stop_date.day)

    for unit in unit_list:
        cursor = mongodb_client.energydb.predictions.find({
            "unit_id": unit,
        })

        for element in cursor:
            # print(element["start_date"])
            # print(start_date_time)
            # print(element["stop_date"])
            # print(stop_date_time)
            # print(type(element["start_date"]))
            if (element["start_date"] > start_date_time and stop_date_time < element["stop_date"]):
                result_list.append({
                    "unit_id": element["unit_id"],
                    "prediction": element["prediction"]
                })

    for element in result_list:
        print(element["prediction"])


def forecast_panel(df_unit, df_weather, stop_date):
    result_list=[]
    pass