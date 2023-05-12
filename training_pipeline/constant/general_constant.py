LABEL = 'survived'

MLFLOW_EXPERIMENT='titanic-ml'
ML_FLOW_TRACKING_URI = "http://localhost:5000"

QUERY_TRAIN_TITANIC_DATA = 'SELECT * FROM titanic where survived != -1'
QUERY_TEST_TITANIC_DATA = 'SELECT * FROM titanic where survived = -1'

FEATURE_PIPELINE_JOBLIB_PATH = "./feature_pipeline/artifact"

X_TRAIN = './feature_pipeline/data/processed/x_train.csv'
X_TEST = './feature_pipeline/data/processed/x_test.csv'
Y_TRAIN = './feature_pipeline/data/processed/y_train.csv'
Y_TEST = './feature_pipeline/data/processed/y_test.csv'

MODEL_URI = "models://{}/{}/{}"
