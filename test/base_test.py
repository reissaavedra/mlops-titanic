from sqlalchemy.engine import Result
from sqlalchemy.orm import Session
from typing import List, Any
import time

from test.fakes.models_fake import ModelsFake


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
        monkeypatch.setattr(Session, "execute", mock)
        monkeypatch.setattr(Result, "fetchall", mock)
        monkeypatch.setattr(Result, "fetchone", mock)
        monkeypatch.setattr(time, "sleep", not_results)

    @staticmethod
    def iterator(results: List[Any]) -> Any:
        result = results[0]
        results.pop(0)
        return result
