import os

FEATURE_PIPELINE_DEFAULT_PATH = f'{os.getcwd()}/ml_engineering/artifacts'

FEATURE_TRAIN_PATH = f'{os.getcwd()}/data/processed/feature_train.csv'
LABEL_TRAIN_PATH = f'{os.getcwd()}/data/processed/label_train.csv'
FEATURE_VALID_PATH = f'{os.getcwd()}/data/processed/feature_valid.csv'
LABEL_VALID_PATH = f'{os.getcwd()}/data/processed/label_valid.csv'

FEATURE_PIPELINE_JOBLIB = '{}/feature_pipeline.joblib'
MODEL_URI = "models://{}/{}/{}"
