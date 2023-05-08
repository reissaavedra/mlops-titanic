import os
import warnings

from database.database import db
from ml_engineering.data_loader.DataLoader import DataLoader
import pandas as pd

from ml_engineering.model.logistic_regression_model import LogisticRegressionModel
from ml_engineering.model.model import Model
from ml_engineering.pipeline.constant.constant import FEATURE_PIPELINE_DEFAULT_PATH
import click
from loguru import logger
import joblib

from ml_engineering.pipeline.training_pipeline.metrics import Metrics
from ml_engineering.pipeline.training_pipeline.train_pipeline import TrainingPipeline
import mlflow

from ml_engineering.pipeline.constant.constant import FEATURE_PIPELINE_DEFAULT_PATH, FEATURE_VALID_PATH, \
    LABEL_TRAIN_PATH, FEATURE_TRAIN_PATH, LABEL_VALID_PATH

from sqlalchemy.orm import Session
from sklearn.pipeline import Pipeline

warnings.simplefilter(action='ignore')

numerical_cols = ['p_class', 'fare']
categorical_cols = ['sex', 'embarked']
columns_remove = ['created_at', 'ticket']
label = 'survived'
query_titanic_train_dataset = f"SELECT * FROM titanic_train"


class TrainExecutor:
    def __init__(self, db: Session, experiment: str):
        self.preprocessor: Pipeline = None
        self.db = db
        self.data_loader = DataLoader(db)
        self.model = None
        self.model_version = None
        self.training_pipeline: TrainingPipeline = None

        mlflow.set_experiment(experiment)

    def load_data(self):
        X_train = pd.read_csv(FEATURE_TRAIN_PATH, index_col=0)
        y_train = pd.read_csv(LABEL_TRAIN_PATH, index_col=0)
        X_valid = pd.read_csv(FEATURE_VALID_PATH, index_col=0)
        y_valid = pd.read_csv(LABEL_VALID_PATH, index_col=0)
        return X_train, y_train, X_valid, y_valid

    def build_training_pipeline_model(self, model: Model):
        self.model = model
        self.training_pipeline = TrainingPipeline(self.model).get_training_pipeline()


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--output', '-o', type=str, default=FEATURE_PIPELINE_DEFAULT_PATH)
@click.option('--experiment', '-e', type=str, default='ml-titanic-experiment')
@click.option('--model-name', '-mn', type=str, default='titanic-log-reg-model')
def main(verbose, output: str, experiment, model_name: str):
    log_reg_params = dict(solver="saga", max_iter=1000)
    log_reg_model = LogisticRegressionModel(model_name=model_name,
                                            **log_reg_params)

    train_executor = TrainExecutor(db=db,
                                   experiment=experiment)

    X_train, y_train, X_valid, y_valid = train_executor.load_data()
    train_executor.build_training_pipeline_model(log_reg_model)

    with mlflow.start_run():
        fitted = train_executor.training_pipeline.fit(X_train, y_train)
        train_preds = fitted.predict(X_train)
        valid_preds = fitted.predict(X_valid)
        metrics = Metrics(y_train, y_valid, train_preds, valid_preds)
        mlflow.log_metrics(metrics.get_metrics())
        mlflow.sklearn.log_model(sk_model=fitted,
                                 artifact_path="log_reg_model",
                                 registered_model_name=train_executor.model.model_name
                                 )
