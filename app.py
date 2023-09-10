import pandas as pd
import pymongo
import streamlit as st

from utils_dir import styles
from utils_dir.texts import text


st.set_page_config(
    page_title="Green Energy Production Forecasting",
    page_icon="🔋",
)


# Initialize database connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_database_connection():
    return pymongo.MongoClient("mongodb://root:pass@0.0.0.0:27017/")


# @st.cache_resource
# def add_turbine_data_to_db(turbine_data):
#
#     mongodb_client.energydb.turbines.insert_many(turbine_data)
#

# mongodb_client = init_database_connection()
# energy_tech_df = pd.read_csv("./data/wind_turbines.csv")
# energy_tech_df = energy_tech_df.drop_duplicates()
# energy_tech_df = energy_tech_df[["Turbine Model", "Tower Height", "Rotor Diameter", "Production Year", "START m/s",
#                                  "STOP  m/s"]]
# energy_tech_df = energy_tech_df.drop_duplicates()
#
# add_turbine_data_to_db(energy_tech_df.to_dict(orient="records"))

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





