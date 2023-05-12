import joblib
import pandas as pd

from feature_pipeline.data_loader.data_loader import DataLoader
from inference_pipeline.constant.general_constant import (
    FEATURE_PIPELINE_JOBLIB_PATH, INFERENCE_DATA_DEFAULT, PROCESSED_DATA,
    QUERY_TEST_TITANIC_DATA, RAW_DATA, REMOVE_COLS)
from inference_pipeline.process.inference_process import InferenceProcess
from training_pipeline.constant.general_constant import MLFLOW_EXPERIMENT
from training_pipeline.facade.mlflow_facade import MLFlowFacade


class TitanicInferenceProcess(InferenceProcess):
    def __init__(self, config):
        self.config = config

    def get_data(self):
        data_loader = DataLoader(self.config.database)
        data = data_loader.get_data(QUERY_TEST_TITANIC_DATA)
        data = data_loader.remove_columns(data, REMOVE_COLS)
        data.to_csv(RAW_DATA, index=False)

    def feature_pipeline(self):
        processor = joblib.load(f'{FEATURE_PIPELINE_JOBLIB_PATH}/feature_pipeline.joblib')
        data = pd.read_csv(RAW_DATA, index_col=False)
        index_data = data['passenger_id']
        data.drop('passenger_id', axis=1)
        processed_data = processor.transform(data)
        processed_data['passenger_id'] = index_data
        processed_data.to_csv(PROCESSED_DATA, index=False)

    def run_inference(self):
        mlflow_facade = MLFlowFacade(self.config.mlflow_tracking_uri, MLFLOW_EXPERIMENT)
        model = mlflow_facade.get_model_by_name(self.config.model_name)
        data = pd.read_csv(PROCESSED_DATA, index_col=False)
        index_data = data['passenger_id']
        data = data.drop('passenger_id', axis=1)
        predictions = model.predict(data)
        data['passenger_id'] = index_data
        data['predictions'] = predictions
        data.to_csv(INFERENCE_DATA_DEFAULT)

    def save_predictions(self):
        raise NotImplementedError()
