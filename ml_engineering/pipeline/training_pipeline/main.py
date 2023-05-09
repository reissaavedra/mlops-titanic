import os
import warnings

from database.database import db
from ml_engineering.data_loader.DataLoader import DataLoader
import pandas as pd

import click

from ml_engineering.pipeline.training_pipeline.metrics import Metrics
import mlflow

from ml_engineering.pipeline.constant.constant import FEATURE_PIPELINE_DEFAULT_PATH, FEATURE_VALID_PATH, \
    LABEL_TRAIN_PATH, FEATURE_TRAIN_PATH, LABEL_VALID_PATH, MODEL_JOBLIB_PATH
import joblib
from sqlalchemy.orm import Session
from sklearn.pipeline import Pipeline
import yaml


from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

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
        self.type_models = dict(
            logistic_regression=LogisticRegression,
            random_forest=RandomForestClassifier,
            xgboost=XGBClassifier
        )

        mlflow.set_experiment(experiment)

    def load_data(self):
        X_train = pd.read_csv(FEATURE_TRAIN_PATH, index_col=0)
        y_train = pd.read_csv(LABEL_TRAIN_PATH, index_col=0)
        X_valid = pd.read_csv(FEATURE_VALID_PATH, index_col=0)
        y_valid = pd.read_csv(LABEL_VALID_PATH, index_col=0)
        return X_train, y_train, X_valid, y_valid

    @staticmethod
    def save_model_local(model, output, name):
        if not os.path.exists(MODEL_JOBLIB_PATH.format(output)):
            os.makedirs(MODEL_JOBLIB_PATH.format(output))
        joblib.dump(model, f'{MODEL_JOBLIB_PATH.format(output)}/{name}.joblib')


@click.command()
@click.option('--type', '-t', type=str, default='logistic_regression')
@click.option('--hyperparams', '-hp', type=str, default='./hyperparams.yaml')
@click.option('--experiment', '-e', type=str, default='ml-titanic-experiment')
@click.option('--name', '-n', type=str, default='titanic-log-reg-model')
def main(experiment, type: str, hyperparams: str, name: str):
    train_executor = TrainExecutor(db=db,
                                   experiment=experiment)
    with open(hyperparams) as f:
        hyperparams = yaml.load(f, Loader=yaml.FullLoader)

    model = train_executor.type_models[type](**hyperparams)

    X_train, y_train, X_valid, y_valid = train_executor.load_data()

    with mlflow.start_run():
        fitted = model.fit(X_train, y_train)
        train_preds = fitted.predict(X_train)
        valid_preds = fitted.predict(X_valid)
        metrics = Metrics(y_train, y_valid, train_preds, valid_preds)
        mlflow.log_metrics(metrics.get_metrics())
        mlflow.sklearn.log_model(sk_model=fitted,
                                 artifact_path="model",
                                 registered_model_name=name
                                 )

    train_executor.save_model_local(fitted, output=FEATURE_PIPELINE_DEFAULT_PATH, name=name)
