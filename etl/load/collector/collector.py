import csv
from abc import ABC, abstractmethod

from etl.constant.general_constant import RAW_DATA_DEFAULT_PATH
from etl.load.repository.titanic_repository import TitanicRepository
from etl.transform.preprocessor import Preprocessor


class DataCollector(ABC):
    target: TitanicRepository

    @abstractmethod
    def pre_processing(self):
        """Method to make pre processing to file e.g. unzip"""

    @abstractmethod
    def load_data(self, file_path: str, titanic_repository: TitanicRepository):
        """Method to make pre processing to file e.g. unzip"""


class TitanicCollector(DataCollector):
    __preprocessor = Preprocessor()

    def pre_processing(self):
        self.__preprocessor.decompress_file(path_input=f'{RAW_DATA_DEFAULT_PATH}/titanic.zip',
                                            path_output=f'{RAW_DATA_DEFAULT_PATH}/uncompressed')

    def load_data(self, file_path: str, titanic_repository: TitanicRepository):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            data = [row for row in reader]
        titanic_repository.bulk_load_data(data)
