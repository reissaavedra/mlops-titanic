import mlflow
from mlflow.tracking import MlflowClient

from training_pipeline.constant.general_constant import (MLFLOW_EXPERIMENT,
                                                         MODEL_URI)


class MLFlowFacade:
    def __init__(self, tracking_uri, experiment):
        self.experiment = experiment
        mlflow.set_registry_uri(tracking_uri)
        mlflow.set_experiment(self.experiment)

    def train_model(self, model, model_name, data, metrics_iterator):
        with mlflow.start_run():
            mlflow.log_params(model.get_params())
            model.fit(data[0], data[1])
            train_predictions = model.predict(data[0])
            test_predictions = model.predict(data[2])
            train_metrics = metrics_iterator.calculate_metrics(train_predictions, data[1], 'train')
            test_metrics = metrics_iterator.calculate_metrics(test_predictions, data[3], 'test')
            mlflow.log_metrics(train_metrics)
            mlflow.log_metrics(test_metrics)
            mlflow.sklearn.log_model(sk_model=model,
                                     artifact_path=f'{self.experiment}/{model_name}-artifact',
                                     registered_model_name=model_name
                                     )

    @staticmethod
    def get_model_by_name(model_name):
        model_version = mlflow.search_model_versions(filter_string=f"name='{model_name}'")[0]
        model_uri = MODEL_URI.format(model_version.run_id, model_version.name, model_version.version)
        return mlflow.pyfunc.load_model(model_uri)
