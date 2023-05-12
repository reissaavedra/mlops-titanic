import mlflow
from mlflow.tracking import MlflowClient

from training_pipeline.factory.model_factory import ModelFactory
import yaml


class MLFlowFacade:
    def __init__(self, tracking_uri):
        self.tracking_uri = tracking_uri
        self.client = MlflowClient(tracking_uri=self.tracking_uri)

    def train_model(self, model, model_type, data, metrics_iterator):
        mlflow.set_registry_uri(self.tracking_uri)
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment('titanic-ml')

        with mlflow.start_run():
            mlflow.log_params(model.get_params())
            model.fit(data[0], data[1])
            train_predictions = model.predict(data[0])
            test_predictions = model.predict(data[2])
            train_metrics = metrics_iterator.calculate_metrics(train_predictions, data[1], 'train')
            test_metrics = metrics_iterator.calculate_metrics(test_predictions, data[3], 'test')
            mlflow.log_metrics(train_metrics)
            mlflow.log_metrics(test_metrics)
            mlflow.sklearn.log_model(model, model_type)

    def get_model_uri(self, run_id):
        run = self.client.get_run(run_id)
        model_uri = f"{self.tracking_uri}/{run.info.artifact_uri}/trained_model"
        return model_uri
