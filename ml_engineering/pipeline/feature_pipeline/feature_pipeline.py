from typing import List

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, Normalizer

from ml_engineering.pipeline.feature_pipeline.transformers.age_column import AgeColumnTransformer
from ml_engineering.pipeline.feature_pipeline.transformers.cabin_column import CabinColumnTransformer
from ml_engineering.pipeline.feature_pipeline.transformers.name_column import NameColumnTransformer
from ml_engineering.pipeline.feature_pipeline.transformers.passenger_column import PassengerColumnTransformer
from ml_engineering.pipeline.feature_pipeline.transformers.categorical_column import CategoricalColumnTransformer


class FeaturePipeline:
    name_transformer = NameColumnTransformer()
    age_transformer = AgeColumnTransformer()
    cabin_transformer = CabinColumnTransformer()
    passenger_transformer = PassengerColumnTransformer()
    categorical_transformer = CategoricalColumnTransformer()
    normalizer = Normalizer().set_output(transform='pandas')

    def __init__(self, numerical_cols: List[str], categorical_cols: List[str]):
        self.numerical_cols = numerical_cols
        self.categorical_cols = categorical_cols

    @staticmethod
    def _set_numerical_transformer():
        return Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean'))])

    @staticmethod
    def _set_categorical_transformer():
        return Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
        ])

    def get_pipeline(self) -> Pipeline:
        return Pipeline(steps=[('name', self.name_transformer),
                               ('age', self.age_transformer),
                               ('cabin', self.cabin_transformer),
                               ('passenger_id', self.passenger_transformer),
                               ('categorical', self.categorical_transformer),
                               ('normalizer', self.normalizer),
                               ])
