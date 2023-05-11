from loguru import logger
from abc import abstractmethod, ABC
from etl.constant.general_constant import ALEMBIC_INI_PATH


class ETLProcess(ABC):
    def execute(self):
        self.pre_etl_process()
        self.extract()
        self.transform()
        self.load()

    @staticmethod
    def pre_etl_process():
        try:
            from alembic.config import Config
            from alembic import command

            alembic_cfg = Config(ALEMBIC_INI_PATH)
            command.downgrade(alembic_cfg, "base")
            command.upgrade(alembic_cfg, "head")
        except Exception as ex:
            logger.error(ex.__str__())
            raise ex

    @abstractmethod
    def extract(self):
        raise NotImplementedError()

    @abstractmethod
    def transform(self):
        raise NotImplementedError()

    @abstractmethod
    def load(self):
        raise NotImplementedError()
