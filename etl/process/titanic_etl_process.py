from etl.constant.general_constant import RAW_DATA_DEFAULT_PATH, TRAIN_CSV_PATH, TEST_CSV_PATH, TRANSFORMATED_PATH
from etl.transform.transformation_strategy import UnionStrategy, FillEmptyStrategy
from etl.transform.transformation_composite import CompositeTransformationStep
from etl.load.repository.titanic_sql_repository import TitanicSqlRepository
from etl.extract.extractor.data_output import LocalPathOutput
from etl.process.etl_process import ETLProcess
from etl.load.model.titanic import Titanic
from loguru import logger
import pandas as pd


class TitanicETLProcess(ETLProcess):

    def __init__(self, config):
        self.config = config

    def extract(self):
        logger.info(f"Extracting data from {self.config.api}")
        api = self.config.api
        path = LocalPathOutput(path=RAW_DATA_DEFAULT_PATH).path
        api.extract(path)
        return path

    def transform(self):
        df_train = pd.read_csv(TRAIN_CSV_PATH)
        logger.info(f'Column rows train: {df_train.shape}')
        df_test = pd.read_csv(TEST_CSV_PATH)
        logger.info(f'Column rows test: {df_test.shape}')
        transform_step = CompositeTransformationStep()
        if self.config.union:
            transform_step.add_step(UnionStrategy())
        if self.config.fill_empty:
            transform_step.add_step(FillEmptyStrategy())
        transformed_data = transform_step.transform([df_train, df_test])
        transformed_data.to_csv(TRANSFORMATED_PATH)
        logger.info(f'Column rows: {transformed_data.shape}')

    def load(self):
        logger.info(f"Loading data to database: {self.config.database}")
        df_transformed_data = pd.read_csv(f'{RAW_DATA_DEFAULT_PATH}/transformed_data.csv')
        titanic_list = [Titanic(passenger_id=int(row['PassengerId']),
                                survived=row['Survived'],
                                p_class=int(row['Pclass']),
                                name=row['Name'],
                                sex=row['Sex'],
                                age=float(row['Age']),
                                sib_sp=int(row['SibSp']),
                                parch=int(row['Parch']),
                                ticket=row['Ticket'],
                                fare=float(row['Fare']),
                                cabin=row['Cabin'],
                                embarked=row['Embarked']) for _, row in df_transformed_data.iterrows()]

        logger.info(f'Lenght array: {len(titanic_list)}')
        __titanic_train_sql_repository = TitanicSqlRepository(self.config.database)
        data_loaded = __titanic_train_sql_repository.bulk_load_data(titanic_list)
        logger.info(f'Lenght data loaded: {len(data_loaded)}')