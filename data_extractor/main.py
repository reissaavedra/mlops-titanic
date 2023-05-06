from data_extractor.constant.general_constant import RAW_DATA_DEFAULT_PATH
from data_extractor.data_output.data_output import LocalPathOutput
from data_extractor.extractor.titanic_data_extractor import TitanicDataExtractor


def start_application():
    local_path_output = LocalPathOutput(path=RAW_DATA_DEFAULT_PATH)
    titanic_data_extractor = TitanicDataExtractor(data_output=local_path_output)
    titanic_data_extractor.get_raw_data()


if __name__ == '__main__':
    start_application()
