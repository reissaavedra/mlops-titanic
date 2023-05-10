import click

from etl.constant.general_constant import RAW_DATA_DEFAULT_PATH, TRAIN_CSV_PATH, TEST_CSV_PATH
from etl.extract.data_output.data_output import LocalPathOutput
from etl.load.collector.collector import TitanicCollector
from etl.load.repository.titanic_train_sql_repository import TitanicTrainSqlRepository
from database.database import db
from etl.load.repository.titanic_test_sql_repository import \
    TitanicTestSqlRepository

from etl.extract.extractor.titanic_data_extractor import TitanicDataExtractor


from loguru import logger




def init_alembic():
    try:
        from alembic.config import Config
        from alembic import command

        alembic_cfg = Config("./etl/alembic.ini")
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")
    except Exception as ex:
        logger.error(ex.__str__())
        raise ex


class LocalETL:
    local_path_output = LocalPathOutput(path=RAW_DATA_DEFAULT_PATH)
    train_sql_repository = TitanicTrainSqlRepository(db=db)
    test_sql_repository = TitanicTestSqlRepository(db=db)
    titanic_data_collector = TitanicCollector()

    def __init__(self,
                 train_csv_path: str,
                 test_csv_path: str,
                 verbose=False):
        init_alembic()
        self.verbose: bool = verbose
        self.train_csv_path = train_csv_path
        self.test_csv_path = test_csv_path

    def extract(self):
        if self.verbose:
            logger.info('Extracting data from Kaggle')
        titanic_data_extractor = TitanicDataExtractor(data_output=self.local_path_output)
        titanic_data_extractor.get_raw_data()

    def transform_and_load(self):
        if self.verbose:
            logger.info('Loading data into postgres database')
        self.titanic_data_collector.pre_processing()
        self.titanic_data_collector.load_data(self.train_csv_path, self.train_sql_repository)
        self.titanic_data_collector.load_data(self.test_csv_path, self.test_sql_repository)

    def exec_etl_pipeline(self):
        self.extract()
        self.transform_and_load()


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--train-path', type=str, default=TRAIN_CSV_PATH, help="Path train dataset")
@click.option('--test-path', type=str, default=TEST_CSV_PATH, help="Path test dataset")
def main(verbose, train_path, test_path):
    etl_local = LocalETL(verbose=verbose, train_csv_path=train_path, test_csv_path=test_path)
    etl_local.exec_etl_pipeline()
