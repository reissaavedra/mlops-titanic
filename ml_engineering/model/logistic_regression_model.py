from dataclasses import dataclass
from functools import lru_cache

import pandas as pd
from joblib import dump, load
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml_engineering.model.model import Model, ModelParams


@dataclass
class LogisticRegressionModelParams(ModelParams):
    params = {
        'train_split': 80
    }


class LogisticRegressionModel(Model):

    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.logisticRegr = LogisticRegression(solver=kwargs['solver'])

    def fit(self,
            x_train: pd.DataFrame,
            y_train: pd.DataFrame):
        return self.logisticRegr.fit(x_train, y_train)

    def predict(self, x_valid: pd.Series):
        return self.logisticRegr.predict(x_valid)
