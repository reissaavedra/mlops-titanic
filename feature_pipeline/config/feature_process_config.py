class FeatureProcessConfig:
    def __init__(self):
        self.database = None
        self.pipeline = None

    def set_feature_pipeline(self, feature_pipeline):
        self.pipeline = feature_pipeline
        return self

    def set_database(self, db):
        self.database = db
        return self

    def build(self):
        return self
