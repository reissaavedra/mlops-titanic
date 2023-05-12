import pandas as pd

from training_pipeline.constant.general_constant import X_TRAIN, X_TEST, Y_TRAIN, Y_TEST, MLFLOW_EXPERIMENT
from training_pipeline.facade.mlflow_facade import MLFlowFacade
from training_pipeline.factory.model_factory import ModelFactory
from training_pipeline.process.training_process import TrainingProcess
import yaml


class TitanicTrainingProcess(TrainingProcess):

    def set_config(self, config):
        self.config = config
        return self

    def get_data(self):
        X_train = pd.read_csv(X_TRAIN)
        X_test = pd.read_csv(X_TEST)
        y_train = pd.read_csv(Y_TRAIN)
        y_test = pd.read_csv(Y_TEST)
        self.data = [X_train, y_train, X_test, y_test]

    def training_pipeline(self):
        mlflow_facade = MLFlowFacade(self.config.mlflow_tracking_uri, MLFLOW_EXPERIMENT)
        factory = ModelFactory()

        model_factory = factory.create_factory(self.config.model_type)
        with open(self.config.hyperparams, "r") as f:
            hyperparams = yaml.safe_load(f)[self.config.model_type]

        model = model_factory.create_model(**hyperparams)
        mlflow_facade.train_model(model,
                                  self.config.model_name,
                                  self.data,
                                  self.config.metrics_iterator)

    def build(self):
        return self

    def evaluate_metrics(self):
        pass
