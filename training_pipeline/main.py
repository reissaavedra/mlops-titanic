import warnings

import click
from loguru import logger

from training_pipeline.config.training_process_config import \
    TrainingProcessConfig
from training_pipeline.constant.general_constant import ML_FLOW_TRACKING_URI
from training_pipeline.process.titanic_training_process import \
    TitanicTrainingProcess

# warnings.filterwarnings(action='ignore')


@click.command()
@click.option('--model_type', '-mt', type=str)
@click.option('--hyperparams', '-hp', type=str, default='./hyperparams.yaml')
@click.option('--model_name', '-mn', type=str)
def main(model_type, hyperparams, model_name):
    logger.info('Loading config...')

    training_config = (TrainingProcessConfig()
                       .set_model_type(model_type)
                       .set_hyperparams(hyperparams)
                       .set_model_name(model_name)
                       .set_mlflow_tracking_uri(ML_FLOW_TRACKING_URI)
                       .set_accuracy_metric()
                       .set_recall_metric())

    training_process = (TitanicTrainingProcess()
                        .set_config(training_config)
                        .build())
    training_process.execute()
