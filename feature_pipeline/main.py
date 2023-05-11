from loguru import logger
import click

from database.database import db
from feature_pipeline.config.feature_pipeline_config import FeaturePipelineConfig
from feature_pipeline.config.feature_process_config import FeatureProcessConfig
from feature_pipeline.pipeline.feature_pipeline_actual import FeaturePipeline
from feature_pipeline.process.titanic_feature_process import TitanicFeatureProcess


@click.command()
def main():
    logger.info('Loading config...')

    feature_config = (FeaturePipelineConfig()
                      .set_name_pipeline(name_pipeline=True)
                      .set_age_pipeline(age_pipeline=True)
                      .set_cabin_pipeline(cabin_pipeline=True)
                      .set_passenger_id_pipeline(passenger_id_pipeline=True)
                      .set_categorical_pipeline(categorical_pipeline=True)
                      .set_normalizer_pipeline(normalizer_pipeline=True))

    pipeline = FeaturePipeline(feature_config)

    config = (FeatureProcessConfig()
              .set_database(db)
              .set_feature_pipeline(pipeline)
              .build())

    titanic_feature_pipeline = TitanicFeatureProcess(config)
    logger.info('Executing Feature process')
    titanic_feature_pipeline.execute()
