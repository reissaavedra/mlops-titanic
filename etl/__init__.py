from dotenv import load_dotenv
from loguru import logger

load_dotenv('./etl/.env')

try:
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config("/home/reisson/TUL/mlops-titanic/etl/alembic.ini")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
except Exception as ex:
    logger.error(ex.__str__())
    raise ex
