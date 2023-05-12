NUMERICAL_COLS = ['p_class', 'fare']
CATEGORICAL_COLS = ['sex', 'embarked']
REMOVE_COLS = ['created_at', 'ticket']
LABEL = 'survived'

RAW_DATA_DEFAULT_PATH: str = "./inference_pipeline/data/raw"
PROCESSED_DATA_DEFAULT_PATH: str = "./inference_pipeline/data/processed"

X_TRAIN_CSV = '/x_train.csv'
X_TEST_CSV = '/x_test.csv'
Y_TRAIN_CSV = '/y_train.csv'
Y_TEST_CSV = '/y_test.csv'

RAW_X_TRAIN = f'{RAW_DATA_DEFAULT_PATH}{X_TRAIN_CSV}'
RAW_X_TEST = f'{RAW_DATA_DEFAULT_PATH}{X_TEST_CSV}'
RAW_Y_TRAIN = f'{RAW_DATA_DEFAULT_PATH}{Y_TRAIN_CSV}'
RAW_Y_TEST = f'{RAW_DATA_DEFAULT_PATH}{Y_TEST_CSV}'

PROCESSED_X_TRAIN = f'{PROCESSED_DATA_DEFAULT_PATH}{X_TRAIN_CSV}'
PROCESSED_X_TEST = f'{PROCESSED_DATA_DEFAULT_PATH}{X_TEST_CSV}'
PROCESSED_Y_TRAIN = f'{PROCESSED_DATA_DEFAULT_PATH}{Y_TRAIN_CSV}'
PROCESSED_Y_TEST = f'{PROCESSED_DATA_DEFAULT_PATH}{Y_TEST_CSV}'

QUERY_TRAIN_TITANIC_DATA = 'SELECT * FROM titanic where survived != -1'
QUERY_TEST_TITANIC_DATA = 'SELECT * FROM titanic where survived = -1'

FEATURE_PIPELINE_JOBLIB_PATH = "./feature_pipeline/artifact"


