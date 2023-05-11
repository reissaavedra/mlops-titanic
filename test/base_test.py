from etl.load.repository.titanic_test_sql_repository import TitanicTestSqlRepository
from etl.load.repository.titanic_sql_repository import TitanicTrainSqlRepository
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session
from typing import List, Any
import time
from alembic.config import Config
from test.fakes.models_fake import ModelsFake
from alembic import command


class BaseTest(ModelsFake):
    def mock_all_externals_db_dynamic(self, monkeypatch, results):
        self.__set_common_mocks(monkeypatch, results)

    def mock_all_externals_db_failed(self, monkeypatch, results):
        self.__set_common_mocks(monkeypatch, results)
        monkeypatch.setattr(Session, "execute", lambda *args, **kwargs: None)

    def mock_all_externals(self, monkeypatch, results):
        self.__set_common_mocks(monkeypatch, results)
        monkeypatch.setattr(Session, "execute", lambda *args, **kwargs: Result(args))

    def __set_common_mocks(self, monkeypatch, results):
        def mock(*args, **kwargs):
            return self.iterator(results)

        def not_results(*args, **kwargs):
            return None

        monkeypatch.setattr(Session, "execute", mock)
        monkeypatch.setattr(Session, "add", mock)
        monkeypatch.setattr(Session, "commit", mock)
        monkeypatch.setattr(Session, "refresh", mock)
        monkeypatch.setattr(Session, "bulk_save_objects", mock)
        monkeypatch.setattr(Result, "fetchall", mock)
        monkeypatch.setattr(Result, "fetchone", mock)
        monkeypatch.setattr(time, "sleep", not_results)
        monkeypatch.setattr(TitanicTrainSqlRepository, "get_all", mock)
        monkeypatch.setattr(TitanicTrainSqlRepository, "get_by_id", mock)
        monkeypatch.setattr(TitanicTrainSqlRepository, "create", mock)
        monkeypatch.setattr(TitanicTrainSqlRepository, "update", mock)
        monkeypatch.setattr(TitanicTrainSqlRepository, "delete", mock)
        monkeypatch.setattr(TitanicTrainSqlRepository, "bulk_load_data", mock)
        monkeypatch.setattr(TitanicTestSqlRepository, "get_all", mock)
        monkeypatch.setattr(TitanicTestSqlRepository, "get_by_id", mock)
        monkeypatch.setattr(TitanicTestSqlRepository, "create", mock)
        monkeypatch.setattr(TitanicTestSqlRepository, "update", mock)
        monkeypatch.setattr(TitanicTestSqlRepository, "delete", mock)
        monkeypatch.setattr(TitanicTestSqlRepository, "bulk_load_data", mock)
        monkeypatch.setattr(Config, '__init__', not_results)
        monkeypatch.setattr(command, 'downgrade', not_results)
        monkeypatch.setattr(command, 'downgrade', not_results)

    @staticmethod
    def iterator(results: List[Any]) -> Any:
        result = results[0]
        results.pop(0)
        return result
