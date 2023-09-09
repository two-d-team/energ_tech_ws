import pandas as pd
import pickle
import numpy as np
import os
import sys
import datetime
import plotly.express as px


current_dir = os.path.dirname(os.path.abspath(__file__))

pages_path = os.path.join(current_dir, 'pages')
sys.path.append(pages_path)

# from page1 import age,gender,score,credit_limit,income,bnr40,offer_crab,offer_delfin,offer_pinguin,produs,other_credits,comission

# model_path = 'model/'
    # with open(model_path + 'credit_risk_model.pkl', 'rb') as file:
    #     model = pickle.load(file)


current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
excel_file_path = f"results_from_{formatted_datetime}.xlsx"

def forecast(unit_list,start_date,stop_date):
    result_list=[]
    pass
    #for unit in unit_list:
        # select data from database for each unit
        #df=where in start date - stop date

        # for row in df.itterrows()
        #     row['forecasted']=model.predict(row)
        #     #result_list.append(result)
        # #result to series
       # #df["Forecasted"]=result_series
        #df.to_excel(excel_file_path, sheet_name=unit, index=False)


        # fig = px.line(df, x="datetime", y="", color='country')
        # fig.show()







    #result to series
    #return result[0]
# print(predict(age,gender,score,credit_limit,income,bnr40,offer_crab,offer_delfin,offer_pinguin,produs,other_credits,comission))
