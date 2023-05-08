import joblib
from sklearn.pipeline import Pipeline

from ml_engineering.model.model import Model
from ml_engineering.pipeline.feature_pipeline.feature_pipeline import FeaturePipeline


class TrainingPipeline:
    def __init__(self, model: Model):
        self.model: Model = model

    def get_training_pipeline(self):
        return Pipeline(steps=[('model', self.model)])
