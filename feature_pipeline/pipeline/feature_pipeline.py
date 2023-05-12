from sklearn.preprocessing import Normalizer

from feature_pipeline.pipeline.composite_feature_pipeline import \
    CompositeFeaturePipeline
from feature_pipeline.pipeline.transformers.age_column import \
    AgeColumnTransformer
from feature_pipeline.pipeline.transformers.cabin_column import \
    CabinColumnTransformer
from feature_pipeline.pipeline.transformers.categorical_column import \
    CategoricalColumnTransformer
from feature_pipeline.pipeline.transformers.name_column import \
    NameColumnTransformer
from feature_pipeline.pipeline.transformers.passenger_column import \
    PassengerColumnTransformer


class FeaturePipeline:

    def __init__(self, config):
        self.config = config

    def transform(self, x_train, x_test, y_train, y_test):
        transform_step = CompositeFeaturePipeline()
        if self.config.name_pipeline:
            transform_step.add_step(('name', NameColumnTransformer()))
        if self.config.age_pipeline:
            transform_step.add_step(('age', AgeColumnTransformer()))

        if self.config.cabin_pipeline:
            transform_step.add_step(('cabin', CabinColumnTransformer()))

        if self.config.passenger_id_pipeline:
            transform_step.add_step(('passenger_id', PassengerColumnTransformer()))

        if self.config.categorical_pipeline:
            transform_step.add_step(('categorical', CategoricalColumnTransformer()))

        if self.config.normalizer_pipeline:
            transform_step.add_step(('normalizer', Normalizer().set_output(transform='pandas')))
        transform_step.fit(x_train, y_train)
        x_train = transform_step.transform(x_train)
        x_test = transform_step.transform(x_test)
        transform_step.save()
        return x_train, x_test, y_train, y_test
