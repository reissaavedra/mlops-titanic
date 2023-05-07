from data_engineering.constant.general_constant import RAW_DATA_DEFAULT_PATH
from data_engineering.extract.data_output.data_output import LocalPathOutput
from data_engineering.load.collector.collector import TitanicCollector
from data_engineering.load.repository.titanic_train_sql_repository import TitanicTrainSqlRepository
from database.database import db
from data_engineering.load.repository.titanic_test_sql_repository import \
    TitanicTestSqlRepository

from data_engineering.extract.extractor.titanic_data_extractor import TitanicDataExtractor


def start_application():
    local_path_output = LocalPathOutput(path=RAW_DATA_DEFAULT_PATH)
    titanic_data_extractor = TitanicDataExtractor(data_output=local_path_output)
    titanic_data_extractor.get_raw_data()

    titanic_data_collector = TitanicCollector()
    titanic_data_collector.pre_processing()

    train_csv_path = './data/raw/uncompressed/train.csv'
    test_csv_path = './data/raw/uncompressed/test.csv'

    train_sql_repository = TitanicTrainSqlRepository(db=db)
    test_sql_repository = TitanicTestSqlRepository(db=db)
    titanic_data_collector.load_data(train_csv_path, train_sql_repository)
    titanic_data_collector.load_data(test_csv_path, test_sql_repository)


if __name__ == '__main__':
    start_application()
