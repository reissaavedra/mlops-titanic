from loguru import logger
import zipfile


class APIExtractor:
    def __init__(self, api, dataset):
        self.api = api
        self.dataset = dataset

    def download_zip(self, output_file):
        self.api.competition_download_files(competition=self.dataset,
                                            path=output_file,
                                            force=True)
        logger.info(f'Data extracted into {output_file}')

    def unzip(self, output_file):
        with zipfile.ZipFile(f'{output_file}/titanic.zip', "r") as zip_ref:
            zip_ref.extractall(output_file)
        logger.info(f'Data unzipped into {output_file}')

    def extract(self, output_file):
        self.download_zip(output_file)
        self.unzip(output_file)

    def __repr__(self):
        return 'ApiExtractor(api=KaggleApi, dataset=titanic)'
