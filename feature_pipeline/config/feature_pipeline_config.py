class FeaturePipelineConfig:
    def __init__(self):
        self.name_pipeline = False
        self.age_pipeline = False
        self.cabin_pipeline = False
        self.passenger_id_pipeline = False
        self.categorical_pipeline = False
        self.normalizer_pipeline = False

    def set_name_pipeline(self, name_pipeline: bool):
        self.name_pipeline = name_pipeline
        return self

    def set_age_pipeline(self, age_pipeline: bool):
        self.age_pipeline = age_pipeline
        return self

    def set_cabin_pipeline(self, cabin_pipeline: bool):
        self.cabin_pipeline = cabin_pipeline
        return self

    def set_passenger_id_pipeline(self, passenger_id_pipeline: bool):
        self.passenger_id_pipeline = passenger_id_pipeline
        return self

    def set_categorical_pipeline(self, categorical_pipeline: bool):
        self.categorical_pipeline = categorical_pipeline
        return self

    def set_normalizer_pipeline(self, normalizer_pipeline: bool):
        self.normalizer_pipeline = normalizer_pipeline
        return self

    def build(self):
        return self
