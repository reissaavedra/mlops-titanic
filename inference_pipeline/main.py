from loguru import logger
import click

from inference_pipeline.config.inference_process_config import InferenceProcessConfig
from database.database import db
from inference_pipeline.constant.general_constant import ML_FLOW_TRACKING_URI
from inference_pipeline.process.titanic_inference_process import TitanicInferenceProcess


@click.command()
@click.option('--model_name', '-mn', type=str)
def main(model_name):
    logger.info('Loading config...')

    inference_config = (InferenceProcessConfig()
                        .set_database(db)
                        .set_model_name(model_name)
                        .set_mlflow_tracking_uri(ML_FLOW_TRACKING_URI))

    inference_process = (TitanicInferenceProcess(inference_config))
    logger.info('Running inference pipeline')
    inference_process.execute()
