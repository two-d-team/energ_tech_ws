from abc import ABC, abstractmethod

import pandas as pd


class IPreprocess(ABC):
    @abstractmethod
    def fit_transform(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def fit(self):
        pass


class TrainingColumnChecker(IPreprocess):
    def __init__(self, columns_of_interest) -> None:
        super().__init__()
        self.columns_of_interest = columns_of_interest

    def __repr__(self) -> str:
        return "[INFO] Start 'TrainingColumnChecker' job."

    def fit(self, X: pd.DataFrame):
        assert all([col in X.columns for col in self.columns_of_interest]), "[ERROR] Specified columns are not present in inputed dataframe."
        self._data = X
        return self
    
    def transform(self):
        if self._data is None:
            raise Exception('The method "fit" should be called first and a dataframe should be passed.')
        
        self._data= self._data[self.columns_of_interest]
        return self._data    
    
    def fit_transform(self, X):
        return self.fit(X).transform()
    

class MonthTransform(IPreprocess):

    def __init__(self) -> None:
        super().__init__()
        self._data = None

    def __repr__(self) -> str:
        return "[INFO] Start 'MonthTransform' job."

    def fit(self, X: pd.DataFrame):
        assert 'date_from' in X.columns, '[ERROR] Columns "date_from" used for month extraction is not present.'
        # assert X['date_from'].dtype, '[ERROR] Columns "date_from" used for month extraction is not present.'

        self._data = X
        return self

    def transform(self):
        if self._data is None:
            raise Exception('The method "fit" should be called first and a dataframe should be passed.')
        
        self._data['month'] = self._data['date_from'].apply(lambda x: x.month)
        return self._data
    
    def fit_transform(self, X):
        return self.fit(X).transform()
    

class HourTransform(IPreprocess):

    def __init__(self) -> None:
        super().__init__()
        self._data = None

    def __repr__(self) -> str:
        return "[INFO] Start 'HourTransform' job."

    def fit(self, X: pd.DataFrame):
        assert 'date_from' in X.columns, '[ERROR] Columns "date_from" used for hour extraction is not present.'
        # assert X['date_from'].dtype, '[ERROR] Columns "date_from" used for hour extraction is not present.'

        self._data = X
        return self

    def transform(self):
        if self._data is None:
            raise Exception('The method "fit" should be called first and a dataframe should be passed.')
        
        self._data['hour'] = self._data['date_from'].apply(lambda x: x.hour)
        return self._data
    
    def fit_transform(self, X):
        return self.fit(X).transform()
    

class DayTransform(IPreprocess):

    def __init__(self) -> None:
        super().__init__()
        self._data = None

    def __repr__(self) -> str:
        return "[INFO] Start 'DayTransform' job."

    def fit(self, X: pd.DataFrame):
        assert 'date_from' in X.columns, '[ERROR] Columns "date_from" used for day extraction is not present.'
        # assert X['date_from'].dtype, '[ERROR] Columns "date_from" used for hour extraction is not present.'

        self._data = X
        return self

    def transform(self):
        if self._data is None:
            raise Exception('The method "fit" should be called first and a dataframe should be passed.')
        
        self._data['day'] = self._data['date_from'].apply(lambda x: x.day)
        return self._data
    
    def fit_transform(self, X):
        return self.fit(X).transform()
    

class DataCleaner(IPreprocess):

    def __init__(self) -> None:
        super().__init__()
        self._data = None

    def __repr__(self) -> str:
        return "[INFO] Start 'DataCleaner' job."

    def fit(self, X: pd.DataFrame):
        assert 'Real Prod(mwh)' in X.columns, '[ERROR] Column "Real Prod(mwh)" used as target is not present.'
        # assert X['Real Prod(mwh)'].dtype, '[ERROR] Columns "Real Prod(mwh)" used for hour extraction is not present.'

        self._data = X
        return self

    def transform(self):
        if self._data is None:
            raise Exception('The method "fit" should be called first and a dataframe should be passed.')
        print(f'[INFO] Shape of dataset before cleaning {self._data.shape}.')
        self._data = self._data.dropna()
        print(f'[INFO] Shape of dataset after cleaning {self._data.shape}.')
        
        return self._data
    
    def fit_transform(self, X):
        return self.fit(X).transform()
    

class Pipeline(IPreprocess):

    def __init__(self, processors) -> None:
        super().__init__()
        self.processors = processors
        self._data = None

    def fit(self, X: pd.DataFrame):
        # assert X['Real Prod(mwh)'].dtype, '[ERROR] Columns "Real Prod(mwh)" used for hour extraction is not present.'

        self._data = X
        return self

    def transform(self):
        if self._data is None:
            raise Exception('The method "fit" should be called first and a dataframe should be passed.')
        
        for processor in self.processors:
            print(processor)
            self._data = processor.fit_transform(self._data)
        
        return self._data
    
    def fit_transform(self, X):
        return self.fit(X).transform()