import os
from typing import List

import click

from database.database import db
from ml_engineering.data_loader.DataLoader import DataLoader
from ml_engineering.pipeline.constant.constant import FEATURE_PIPELINE_DEFAULT_PATH, FEATURE_VALID_PATH, \
    LABEL_TRAIN_PATH, FEATURE_TRAIN_PATH, LABEL_VALID_PATH, FEATURE_PIPELINE_JOBLIB
from ml_engineering.pipeline.feature_pipeline.feature_pipeline import FeaturePipeline
import joblib
from loguru import logger
from sqlalchemy.orm import Session
from sklearn.pipeline import Pipeline
import warnings

warnings.simplefilter(action='ignore')

numerical_cols = ['p_class', 'fare']
categorical_cols = ['sex', 'embarked']
columns_remove = ['created_at', 'ticket']
label = 'survived'
query_titanic_train_dataset = f"SELECT * FROM titanic_train"


class FeatureExecutor:
    def __init__(self, db: Session):
        self.preprocessor: Pipeline = None
        self.db = db
        self.data_loader = DataLoader(db)
        self.model = None
        self.model_version = None
        self.feature_pipeline = FeaturePipeline(numerical_cols=numerical_cols,
                                                categorical_cols=categorical_cols).get_pipeline()
        self.preprocessor: Pipeline = None

    def preprocess_data(self, query: str, remove_columns: List):
        data = self.data_loader.get_data(query)
        data = self.data_loader.remove_columns(data, remove_columns)
        X_train, X_valid, y_train, y_valid = self.data_loader.train_test_split(data, label=label, random_state=10)
        return X_train, X_valid, y_train, y_valid

    def execute_pipeline(self, X_train, X_valid, y_train, y_valid):
        self.preprocessor = self.feature_pipeline.fit(X_train, y_train)
        X_train_fitted = self.preprocessor.transform(X_train)
        X_valid_fitted = self.preprocessor.transform(X_valid)
        return X_train_fitted, X_valid_fitted, y_train, y_valid

    def save_pipeline(self, output):
        if not os.path.exists(output):
            os.makedirs(output)
        joblib.dump(self.feature_pipeline,
                    FEATURE_PIPELINE_JOBLIB.format(output))

    @staticmethod
    def save_data_processed(X_train, X_valid, y_train, y_valid):
        X_train.to_csv(FEATURE_TRAIN_PATH)
        y_train.to_csv(LABEL_TRAIN_PATH)
        X_valid.to_csv(FEATURE_VALID_PATH)
        y_valid.to_csv(LABEL_VALID_PATH)


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--output', '-o', type=str, default=FEATURE_PIPELINE_DEFAULT_PATH, help="Will print verbose messages.")
def main(verbose, output: str):
    feature_executor = FeatureExecutor(db)

    X_train, X_valid, y_train, y_valid = feature_executor.preprocess_data(query=query_titanic_train_dataset,
                                                                          remove_columns=columns_remove)

    X_train, X_valid, y_train, y_valid = feature_executor.execute_pipeline(X_train, X_valid, y_train, y_valid)

    feature_executor.save_data_processed(X_train, X_valid, y_train, y_valid)
    feature_executor.save_pipeline(output)
