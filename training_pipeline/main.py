from loguru import logger
import click

from training_pipeline.config.training_process_config import TrainingProcessConfig
from training_pipeline.constant.general_constant import ML_FLOW_TRACKING_URI
from training_pipeline.process.titanic_training_process import TitanicTrainingProcess
import warnings

warnings.filterwarnings(action='ignore')


@click.command()
@click.option('--model_type', '-mt', type=str)
@click.option('--hyperparams', '-hp', type=str)
def main(model_type, hyperparams):
    logger.info('Loading config...')

    training_config = (TrainingProcessConfig()
                       .set_model_type(model_type)
                       .set_hyperparams(hyperparams)
                       .set_mlflow_tracking_uri(ML_FLOW_TRACKING_URI)
                       .set_accuracy_metric()
                       .set_recall_metric())

    training_process = (TitanicTrainingProcess()
                        .set_config(training_config)
                        .build())
    training_process.execute()
