from typing import List

import click
import pandas as pd

from database.database import db
from ml_engineering.data_loader.DataLoader import DataLoader
from ml_engineering.pipeline.constant.constant import FEATURE_PIPELINE_DEFAULT_PATH, FEATURE_PIPELINE_JOBLIB, MODEL_URI
import joblib
import warnings
import mlflow
from sqlalchemy import Column, Integer, SmallInteger, String
from database.database import Base
from sqlalchemy.orm import Session
from sklearn.pipeline import Pipeline

warnings.simplefilter(action='ignore')

numerical_cols = ['p_class', 'fare']
categorical_cols = ['sex', 'embarked']
columns_remove = ['created_at', 'ticket']
query_titanic_test_dataset = f"SELECT * FROM titanic_test"


class SurvivedPrediction(Base):
    __tablename__ = "survived_predictions"

    passenger_id = Column(Integer, primary_key=True)
    predict = Column(SmallInteger)
    model = Column(String(250), primary_key=True)


class InferenceExecutor:
    def __init__(self, db: Session):
        self.preprocessor: Pipeline = None
        self.db = db
        self.data_loader = DataLoader(db)
        self.model = None
        self.model_version = None

    def preprocess_data(self, query: str, remove_columns: List, index: str):
        data = self.data_loader.get_data(query)
        data = self.data_loader.remove_columns(data, remove_columns)
        index = data[index]
        return data, index

    def load_pipeline(self, path_feature_pipeline_joblib: str):
        self.preprocessor = joblib.load(FEATURE_PIPELINE_JOBLIB.format(path_feature_pipeline_joblib))

    def transform_data(self, data: pd.DataFrame):
        return self.preprocessor.transform(data)

    def load_latest_model(self, model_name: str):
        model_version = mlflow.search_model_versions(filter_string=f"name='{model_name}'")[0]
        model_uri = MODEL_URI.format(model_version.run_id, model_version.name, model_version.version)
        self.model_version = model_version
        self.model = mlflow.pyfunc.load_model(model_uri)

    def predict(self, data: pd.DataFrame):
        return self.model.predict(data)

    def save_predictions(self, y_predict, idx_predict):
        y_pred = pd.DataFrame({'predict': y_predict,
                               'passenger_id': idx_predict,
                               'model': f'{self.model_version.name} v{self.model_version.version}'
                               })
        survive_preds = [SurvivedPrediction(**row.to_dict()) for _, row in y_pred.iterrows()]
        db.bulk_save_objects(survive_preds)


@click.command()
@click.option('--modelname', '-model', type=str, default="titanic-log-reg-model", help="Name of model")
def main(modelname: str):
    inf_executor = InferenceExecutor(db=db)
    X_test, idx_X_Test = inf_executor.preprocess_data(query=query_titanic_test_dataset,
                                                      remove_columns=columns_remove,
                                                      index='passenger_id')

    inf_executor.load_pipeline(FEATURE_PIPELINE_DEFAULT_PATH)
    X_test = inf_executor.transform_data(X_test)
    inf_executor.load_latest_model(model_name=modelname)

    y_predict_test = inf_executor.predict(X_test)

    inf_executor.save_predictions(y_predict_test, idx_X_Test)
