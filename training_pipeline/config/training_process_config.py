from training_pipeline.metrics.metrics_strategy import (
    AccuracyStrategy, F1ScoreStrategy, MetricsStrategyIterator,
    PrecisionStrategy, RecallStrategy)


class TrainingProcessConfig:
    def __init__(self):
        self.model_type = None
        self.hyperparams = None
        self.mlflow_tracking_uri = None
        self.model_name = None
        self.metrics_iterator = MetricsStrategyIterator()
        self.accuracy_metric = False
        self.precision_metric = False
        self.recall_metric = False
        self.f1_score_metric = False

    def set_model_type(self, model_type):
        self.model_type = model_type
        return self

    def set_model_name(self, model_name):
        self.model_name = model_name
        return self

    def set_hyperparams(self, hyperparams):
        self.hyperparams = hyperparams
        return self

    def set_mlflow_tracking_uri(self, mlflow_tracking_uri):
        self.mlflow_tracking_uri = mlflow_tracking_uri
        return self

    def set_accuracy_metric(self, accuracy_metric=True):
        if accuracy_metric:
            self.metrics_iterator.add_strategy(AccuracyStrategy())
        return self

    def set_f1_score_metric(self, f1_score_metric=True):
        if f1_score_metric:
            self.metrics_iterator.add_strategy(F1ScoreStrategy())
        return self

    def set_precision_metric(self, precision_metric=True):
        if precision_metric:
            self.metrics_iterator.add_strategy(PrecisionStrategy())
        return self

    def set_recall_metric(self, recall_metric=True):
        if recall_metric:
            self.metrics_iterator.add_strategy(RecallStrategy())
        return self

    def build(self):
        return self
