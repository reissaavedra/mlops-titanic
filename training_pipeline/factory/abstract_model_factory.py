from abc import ABC, abstractmethod

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


class AbstractModelFactory(ABC):
    @abstractmethod
    def create_model(self, **kwargs):
        raise NotImplementedError


class LogisticRegressionFactory(AbstractModelFactory):
    def create_model(self, **kwargs):
        return LogisticRegression(**kwargs)


class RandomForestFactory(AbstractModelFactory):
    def create_model(self, **kwargs):
        return RandomForestClassifier(**kwargs)


class XgBoostFactory(AbstractModelFactory):
    def create_model(self, **kwargs):
        return XGBClassifier(**kwargs)
