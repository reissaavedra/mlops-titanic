from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class ModelParams(ABC):
    params: dict


class Model(ABC):
    model_name: str

    @abstractmethod
    def fit(self,
            x_train: pd.DataFrame,
            y_train: pd.DataFrame):
        """Make a prediction from model"""

    @abstractmethod
    def predict(self, x_valid: pd.DataFrame):
        """Make a prediction from model"""
