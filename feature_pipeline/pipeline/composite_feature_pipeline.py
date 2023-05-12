import os

import joblib
from loguru import logger
from sklearn.pipeline import Pipeline

from feature_pipeline.constant.general_constant import \
    FEATURE_PIPELINE_JOBLIB_PATH


class CompositeFeaturePipeline:
    def __init__(self):
        self.steps = []
        self.pipeline = None

    def add_step(self, step):
        self.steps.append(step)

    def fit(self, x_data, y_data):
        self.pipeline = Pipeline(steps=self.steps)
        self.pipeline.fit(x_data, y_data)

    def transform(self, x_data):
        return self.pipeline.transform(x_data)

    def save(self):
        logger.info(f'Saving pipeline into {FEATURE_PIPELINE_JOBLIB_PATH}feature_pipeline.joblib"')
        if not os.path.exists(FEATURE_PIPELINE_JOBLIB_PATH):
            os.makedirs(FEATURE_PIPELINE_JOBLIB_PATH)
        joblib.dump(self.pipeline, f'{FEATURE_PIPELINE_JOBLIB_PATH}/feature_pipeline.joblib')
