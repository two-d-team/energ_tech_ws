import streamlit as st
import pymongo


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb://root:pass@0.0.0.0:27017/")


mongodb_client = init_connection()
mongodb_client.unitsdb.test_collection.insert_one({"name": "Abc", "type": "Wind"})


# Uses st.cache_data to only rerun when the query changes or after 10 minutes.
@st.cache_data(ttl=600)
def get_data():
    test_database = mongodb_client.unitsdb

    return list(test_database.test_collection.find())


units = get_data()


for unit in units:
    st.write("{} has a :{}:".format(unit["name"], unit["type"]))
