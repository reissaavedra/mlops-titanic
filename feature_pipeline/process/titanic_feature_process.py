import pandas as pd

from feature_pipeline.constant.general_constant import QUERY_TRAIN_TITANIC_DATA, REMOVE_COLS, LABEL, RAW_Y_TEST, \
    RAW_Y_TRAIN, RAW_X_TEST, RAW_X_TRAIN, PROCESSED_Y_TRAIN, PROCESSED_Y_TEST, PROCESSED_X_TEST, PROCESSED_X_TRAIN, \
    RAW_DATA_DEFAULT_PATH, PROCESSED_DATA_DEFAULT_PATH
from feature_pipeline.data_loader.data_loader import DataLoader
from feature_pipeline.process.feature_process import FeatureProcess
import os


class TitanicFeatureProcess(FeatureProcess):

    def __init__(self, config):
        self.config = config

    def pre_process_data(self):
        """Method to get data from database and return train_test_split into csv."""
        data_loader = DataLoader(self.config.database)
        data = data_loader.get_data(QUERY_TRAIN_TITANIC_DATA)
        data = data_loader.remove_columns(data, REMOVE_COLS)
        if not os.path.exists(RAW_DATA_DEFAULT_PATH):
            os.makedirs(RAW_DATA_DEFAULT_PATH)
        X_train, X_test, y_train, y_test = data_loader.train_test_split(data, label=LABEL, random_state=10)
        X_train.to_csv(RAW_X_TRAIN, index=False)
        X_test.to_csv(RAW_X_TEST, index=False)
        y_train.to_csv(RAW_Y_TRAIN, index=False)
        y_test.to_csv(RAW_Y_TEST, index=False)

    def execute_feature_pipeline(self):
        X_train = pd.read_csv(RAW_X_TRAIN)
        X_test = pd.read_csv(RAW_X_TEST)
        y_train = pd.read_csv(RAW_Y_TRAIN)
        y_test = pd.read_csv(RAW_Y_TEST)

        X_train, X_test, y_train, y_test = self.config.pipeline.transform(X_train, X_test, y_train, y_test)

        if not os.path.exists(PROCESSED_DATA_DEFAULT_PATH):
            os.makedirs(PROCESSED_DATA_DEFAULT_PATH)
        X_train.to_csv(PROCESSED_X_TRAIN, index=False)
        X_test.to_csv(PROCESSED_X_TEST, index=False)
        y_train.to_csv(PROCESSED_Y_TRAIN, index=False)
        y_test.to_csv(PROCESSED_Y_TEST, index=False)
