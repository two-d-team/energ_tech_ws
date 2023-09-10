from scipy.interpolate import interp1d
import pandas as pd
import json
import os

ROOT = 'data/'

def get_power_curve_pred(pcc_mapper, pcw_mapper, unit_model_map, mapper):
    datetime_all = []
    unit_all = []
    y_pred_all = []

    for unit, df in mapper.items():
        model = unit_model_map[unit]
        pcc = pcc_mapper[model]
        w = pcw_mapper[unit]
        pcc = pd.DataFrame(pcc, columns=['wind_speed', 'power'])
        df = mapper[unit]

        interp_func = interp1d(pcc['wind_speed'], pcc['power'], kind='linear', bounds_error=False, fill_value="extrapolate")
        y_pred = interp_func(df['wind_speed (m/s)']) / 1000 * w

        # y_pred[X['Service'].notna()] = 0
        y_pred[y_pred < 0] = 0

        unit_all.extend(len(y_pred) * [unit])
        y_pred_all.extend(list(y_pred))
        datetime_all.extend(df['date_from'])

    result = pd.DataFrame({
        'wind_plant': unit_all,
        'date_from': datetime_all,
        'Forecast(mwh)': y_pred_all
    })

    return result


def read_unit_config():
    path = 'settings/unit_config.json'

    with open(path, 'r') as f:
        data = json.load(f)
   
    return data


def read_data():
    mapper = {}

    for unit in os.listdir(ROOT):
        print(ROOT + unit)
        df = pd.read_excel(ROOT + unit)
        unit_name = df.wind_plant.unique()[0]
        mapper[unit_name] = df
    
    return mapper


def fix_column_tipo(mapper):
    for unit in list(mapper.keys()):
        mapper[unit] = mapper[unit].rename(columns={'Forecast (mwh)': 'Forecast(mwh)'})
    return mapper



SELECTED_FEATURES_TRAINING = [
    'wind_speed (m/s)', 'wind_dir', 'temp', 'pressure', 'Tower Height', 'Rotor Diameter',
    'Real Prod(mwh)', 'date_from', 'date_to'
]