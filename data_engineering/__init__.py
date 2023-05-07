from loguru import logger

try:
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
except Exception as ex:
    logger.error(ex.__str__())
    raise ex
