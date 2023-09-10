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

mongodb_client.energydb.predictions.insert_many(predictions_sample)


def forecast(unit_list, start_date, stop_date):
    result_list = []
    start_date_time = datetime(start_date.year, start_date.month, start_date.day)
    stop_date_time = datetime(stop_date.year, stop_date.month, stop_date.day)

    for unit in unit_list:
        cursor = mongodb_client.energydb.predictions.find({
            "unit_id": unit
            #"start_date": {"$lte": stop_date_time, "$gte": start_date_time}
        })

        for element in cursor:
            result_list.append({
                "unit_id": element["unit_id"],
                "prediction": element["prediction"]
            })

    for element in result_list:
        print(element["prediction"])
