from training_pipeline.factory.abstract_model_factory import RandomForestFactory, XgBoostFactory, \
    LogisticRegressionFactory


class ModelFactory:
    @staticmethod
    def create_factory(model_type):
        if model_type == "logistic_regression":
            return LogisticRegressionFactory()
        if model_type == "xg_boost":
            return XgBoostFactory()
        if model_type == "random_forest":
            return RandomForestFactory()
        raise ValueError("Invalid model type.")
