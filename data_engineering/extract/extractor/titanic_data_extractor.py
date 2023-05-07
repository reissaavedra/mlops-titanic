from dataclasses import dataclass

from kaggle import KaggleApi

from data_engineering.constant.general_constant import TITANIC_DATASET_NAME
from data_engineering.extract.data_output.data_output import DataOutput
from data_engineering.extract.extractor.data_extractor import DataExtractor
from data_engineering.extract.service.kaggle_service import kaggle_api


@dataclass
class TitanicDataExtractor(DataExtractor):
    data_output: DataOutput
    __kaggle_api: KaggleApi = kaggle_api
    __dataset_name: str = TITANIC_DATASET_NAME

    def get_raw_data(self):
        self.__kaggle_api.competition_download_files(competition=self.__dataset_name,
                                                     path=self.data_output.path,
                                                     force=True)
