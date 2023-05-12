from etl.constant.general_constant import TITANIC_DATASET_NAME
from etl.process.titanic_etl_process import TitanicETLProcess
from etl.extract.extractor.api_extractor import APIExtractor
from etl.extract.service.kaggle_service import kaggle_api
from etl.config.etl_config import ETLConfig
from database.database import db
from loguru import logger
import click


@click.command()
def main():
    logger.info('Loading config')
    config = (ETLConfig()
              .set_build_alembic(True)
              .set_api(APIExtractor(api=kaggle_api, dataset=TITANIC_DATASET_NAME))
              .set_union(True)
              .set_fill_empty(True)
              .set_database(db)
              .build())

    titanic_etl = TitanicETLProcess(config)
    logger.info('Executing ETL process')
    titanic_etl.execute()
