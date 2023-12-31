import streamlit as st
import sys
import os
import datetime
from prediction import predict_sun, predict_turbine

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

from utils_dir.styles import custom_headers


if 'pred_df' not in st.session_state:
    st.session_state.pred_df = None


st.markdown(custom_headers, unsafe_allow_html=True)


st.markdown("<h1>Predict for historical data</h1>", unsafe_allow_html=True)
# from prediction import predict
# st.set_page_config(
#     page_title="Form",
#     page_icon="📝"
# )
#


selected_option=st.radio('Pick one:', ['Wind Turbine','Solar Panel'])
unit_list=[]
start_date=None
stop_date=None

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
        dummy_data = ['Unit1', 'Unit2', 'Unit3', 'Unit4', 'Unit5', 'Unit6', 'Unit7']
        st.session_state['dummy_data'] = dummy_data
    else:
        dummy_data = st.session_state['dummy_data']

    checkbox_container(dummy_data)
    st.write('You selected:')
    unit_list = get_selected_checkboxes()

    st.subheader('Select Start/Stop Dates')

    start_date = st.date_input("Start Date", datetime.date(2023, 9, 9))
    stop_date = st.date_input("Stop Date", datetime.date(2023, 9, 9))

    st.button("Predict",on_click=lambda: predict_turbine(unit_list, start_date, stop_date))

    # if st.button("Predict", key="predict_button_2"):
    #     predict_turbine(unit_list, start_date, stop_date)

    if st.session_state.pred_df is not None:
        csv = st.session_state.pred_df.to_csv(index=False)
        st.download_button(
            label="Download Forecast Data",
            data=csv,
            file_name="forecast_data.csv",
            mime="text/csv",
        )

elif selected_option=="Solar Panel":

    if 'sun_data' not in st.session_state.keys():
        sun_data = ['Unit1']
        st.session_state['sun_data'] = sun_data
    else:
        sun_data = st.session_state['sun_data']

    checkbox_container(sun_data)
    st.write('You selected:')
    #unit_list = get_selected_checkboxes()
    st.subheader('Select Start/Stop Dates')

    start_date = st.date_input("Start Date", datetime.date(2023, 9, 9))
    stop_date = st.date_input("Stop Date", datetime.date(2023, 9, 9))

    st.button("Predict", on_click=predict_sun(unit_list, start_date, stop_date))



