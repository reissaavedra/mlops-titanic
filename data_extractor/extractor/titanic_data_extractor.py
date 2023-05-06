from dataclasses import dataclass

from kaggle import KaggleApi

from data_extractor.constant.general_constant import TITANIC_DATASET_NAME
from data_extractor.data_output.data_output import DataOutput
from data_extractor.extractor.data_extractor import DataExtractor
from data_extractor.service.kaggle_service import kaggle_api


@dataclass
class TitanicDataExtractor(DataExtractor):
    data_output: DataOutput
    __kaggle_api: KaggleApi = kaggle_api
    __dataset_name: str = TITANIC_DATASET_NAME

    def get_raw_data(self):
        self.__kaggle_api.dataset_download_files(self.__dataset_name,
                                                 path=self.data_output.path,
                                                 unzip=False)

    def push_data_to_collector(self):
        pass
