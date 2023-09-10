import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from utils_dir.units import df

key = "e30aa58c263e451988d185745230909"
#q = "47.034746,28.421021"

hourwise_meteo_jsons = []

# generate dates for required period daily
def get_forecast_weather_sun(nr_days,unit_list):
    q=None
    result_df=None
    start_date = datetime.now()
    flag=0
    for unit in unit_list:
        q = df["lattitude"] + "," + df["longitute"]
    response =requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={q}&days={nr_days}&aqi=no&alerts=no")
    if response.status_code == 200:
        result = response.json()
        hourwise_meteo_jsons.append(response.json()["forecast"]["forecastday"][0]["hour"])
    else:
        print(f"request failed with response {response}")

    global_meteo_df = pd.DataFrame(hourwise_meteo_jsons[0])

    for index in range(1, len(hourwise_meteo_jsons)):
        cur_df = pd.DataFrame(hourwise_meteo_jsons[index])
        global_meteo_df = pd.concat([global_meteo_df, cur_df], ignore_index=True)
    if flag == 0:
        result_df=global_meteo_df
        #print (result)
        #rint(global_meteo_df)
        flag=1
    elif flag==1:
        result_df = pd.concat([result_df, global_meteo_df], ignore_index=True)
        # print(result_df)

    result_df.to_excel("output.xlsx")
    return df,result_df




def get_forecast_weather_wind(nr_days, unit_list):
    result_df = None
    start_date = datetime.now()
    flag = 0
    for unit in unit_list:
        q = df["lattitude"] + "," + df["longitute"]

        response = requests.get(
            f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={q}&days={nr_days}&aqi=no&alerts=no")
        if response.status_code == 200:
            result = response.json()
            hourwise_meteo_jsons.append(response.json()["forecast"]["forecastday"][0]["hour"])
        else:
            print(f"request failed with response {response}")

        global_meteo_df = pd.DataFrame(hourwise_meteo_jsons[0])

        for index in range(1, len(hourwise_meteo_jsons)):
            cur_df = pd.DataFrame(hourwise_meteo_jsons[index])
            global_meteo_df = pd.concat([global_meteo_df, cur_df], ignore_index=True)
        if flag == 0:
            result_df = global_meteo_df
            # print (result)
            # rint(global_meteo_df)
            flag = 1
        elif flag == 1:
            result_df = pd.concat([result_df, global_meteo_df], ignore_index=True)
            # print(result_df)

        result_df.to_excel("output.xlsx")
        return df, result_df

#weather_df = get_forecast_weather(number_days, coordinates)
    #global_meteo_df.to_excel("output.xlsx")

    #return result_df

