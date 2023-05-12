class InferenceProcessConfig:
    def __init__(self):
        self.database = None
        self.model_name = None
        self.mlflow_tracking_uri = None

    def set_database(self, db):
        self.database = db
        return self

    def set_model_name(self, model_name):
        self.model_name = model_name
        return self

    def set_mlflow_tracking_uri(self, mlflow_tracking_uri):
        self.mlflow_tracking_uri = mlflow_tracking_uri
        return self

    def build(self):
        return self
