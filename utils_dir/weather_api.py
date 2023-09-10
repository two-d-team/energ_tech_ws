import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from utils_dir.units import df
import pytz

key = "e30aa58c263e451988d185745230909"
#q = "47.034746,28.421021"

def map_wind_meteo_cols(meteo_df):
    meteo_df = meteo_df.copy()
    meteo_df.drop(columns='wind_dir', inplace=True)
    meteo_df.rename(columns={
        'temp_c': 'temp',
        'wind_degree': 'wind_dir',
        'wind_kph': 'wind_speed (m/s)',
        'pressure_mb': 'pressure',
        'time': 'date_from'
    }, inplace=True)

    meteo_df['wind_speed (m/s)'] *= 5.0/18

    return meteo_df[['date_from', 'latitude', 'longitude', 'temp', 'wind_dir', 'wind_speed (m/s)', 'pressure']]


# generate dates for required period daily
def get_forecast_weather_sun(nr_days, unit_list):
    hourwise_meteo_jsons = []

    for unit in unit_list:
        unit_s = df[df.wind_plant == unit].first()

        q = unit_s["latitude"] + "," + unit_s["longitude"]

        response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={q}&days={nr_days}&aqi=no&alerts=no")

        if response.status_code == 200:
            result = response.json()
            json_hours = result["forecast"]["forecastday"][0]["hour"]
            print(response.status_code)
            for d in json_hours:
                d['latitude'] = unit_s["latitude"]
                d['longitude'] = unit_s["longitude"]

            print(json_hours[0])

            hourwise_meteo_jsons.extend(json_hours)
        else:
            print(f"request failed with response {response}")

    global_meteo_df = pd.DataFrame(hourwise_meteo_jsons)
    global_meteo_df.to_excel("output.xlsx")

    return df,global_meteo_df




def get_forecast_weather_wind(nr_days, unit_list):
    hourwise_meteo_jsons = []

    for unit in unit_list:
        unit_s = df[df.wind_plant == unit].iloc[0]

        q = unit_s["latitude"] + "," + unit_s["longitude"]

        response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={q}&days={nr_days}&aqi=no&alerts=no")
        print(f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={q}&days={nr_days}&aqi=no&alerts=no")
        print("\n\n!\n\n\n!\n")
        if response.status_code == 200:
            result = response.json()

            for day in range(len(result["forecast"]["forecastday"])):
                json_hours = result["forecast"]["forecastday"][day]["hour"]

                for d in json_hours:
                    d['latitude'] = unit_s["latitude"]
                    d['longitude'] = unit_s["longitude"]

                hourwise_meteo_jsons.extend(json_hours)
        else:
            print(f"request failed with response {response}")

    global_meteo_df = pd.DataFrame(hourwise_meteo_jsons)
    global_meteo_df = map_wind_meteo_cols(global_meteo_df)
    global_meteo_df.to_excel("output.xlsx")

    return df,global_meteo_df

#weather_df = get_forecast_weather(number_days, coordinates)
    #global_meteo_df.to_excel("output.xlsx")

    #return result_df

