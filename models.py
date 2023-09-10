from abc import ABC, abstractmethod

import lightgbm
import xgboost
from preprocess import DataCleaner, DayTransform, HourTransform, MonthTransform, Pipeline, TrainingColumnChecker

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

from utils import SELECTED_FEATURES_TRAINING, fix_column_tipo, get_power_curve_pred, read_data, read_unit_config

sns.set_style('darkgrid')


class IModel(ABC):

    @abstractmethod
    def initialize_model():
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass


class EvaluateModel:

    def plot(self, y_pred, y_true, model_name, unit):
        plt.figure(figsize=(16, 8))

        plt.plot(y_pred, c='blue')
        plt.plot(y_true.values, c='red')

        plt.legend(['Forecast', 'Prediction'])
        plt.title(model_name + ' ' + unit)
        plt.savefig(model_name + ' ' + unit + ".png")

    def evaluate(self, y_pred, y_true, model_name, unit):

        self.plot(y_pred=y_pred, y_true=y_true, model_name=model_name, unit=unit)

        mae = mean_absolute_error(y_pred, y_true)
        mse = mean_squared_error(y_pred, y_true, squared=False)

        print(f'[INFO] {model_name} Mean absolute error: ', mae)
        print(f'[INFO] {model_name} Mean squared error', mse)   
        return mae, mse


class LightGBMForecast(IModel):

    def __init__(self, learning_rate, max_depth, n_estimators, *args, **kwargs) -> None:
        super().__init__()
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.n_estimators = n_estimators
        self.kwargs = kwargs
        self._model = None

    def initialize_model(self):
        self._model = lightgbm.LGBMRegressor(
            learning_rate=self.learning_rate, 
            max_depth=self.max_depth,
            n_estimators=self.n_estimators,
            **self.kwargs
            )
    
    def fit(self, X, y):
        self._model.fit(X, y)

    def predict(self, X):
        return self._model.predict(X)
    

class XGBoostForecast(IModel):

    def __init__(self, learning_rate, max_depth, n_estimators, *args, **kwargs) -> None:
        super().__init__()
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.n_estimators = n_estimators
        self.kwargs = kwargs
        self._model = None

    def initialize_model(self):
        self._model = xgboost.XGBRegressor(
            learning_rate=self.learning_rate, 
            max_depth=self.max_depth,
            n_estimators=self.n_estimators,
            **self.kwargs
            )
    
    def fit(self, X, y):
        self._model.fit(X, y)

    def predict(self, X):
        return self._model.predict(X)


mapper = read_data()
mapper = fix_column_tipo(mapper)
# mapper = {unit: mapper[unit] for unit in list(mapper.keys())[:-1]}
unit_config = read_unit_config()

pipeline = Pipeline(processors=[TrainingColumnChecker(SELECTED_FEATURES_TRAINING), MonthTransform(), 
                        HourTransform(), DayTransform(),
                        DataCleaner()])

processed_mapper = {}
models_dict = {}

for unit in list(mapper.keys()):
    processed_data = pipeline.fit_transform(mapper[unit])
    processed_mapper[unit] = processed_data
    print(processed_data.shape)
    # print(processed_data.columns, '!!!')


    for processed_unit in list(processed_mapper.keys()):
        df = processed_mapper[processed_unit].copy()
        df = df.drop(['date_from', 'date_to', 'Tower Height', 'Rotor Diameter'], axis=1)
        df = df[df['Real Prod(mwh)'].notna()].copy()

        # X_train, X_test, y_train, y_test = split_data(df, split=694)
        X, y = df.drop('Real Prod(mwh)', axis=1), df['Real Prod(mwh)']

        lightgbm_forecast = LightGBMForecast(learning_rate=0.05, max_depth=3, n_estimators=800)
        lightgbm_forecast.initialize_model()
        lightgbm_forecast.fit(X, y)

        models_dict[unit] = lightgbm_forecast


print('reading unit config...')
unit_config = read_unit_config()
power_curve_pred = get_power_curve_pred(unit_config['power_curve_coef'],
                                        unit_config['power_curve_weights'],
                                        unit_config['unit_model_map'],
                                        mapper)
