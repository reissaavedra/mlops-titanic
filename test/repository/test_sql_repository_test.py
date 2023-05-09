from typing import Any, List

import pytest
from database.database import database

from sqlalchemy.orm import Session
from etl.load.repository.titanic_test_sql_repository import TitanicTestSqlRepository
from test.base_test import BaseTest
from test.fakes.models_fake import ModelsFake
from database.database import db


class TestSqlRepositoryTest(BaseTest):
    __db = db
    __test_sql_repository = TitanicTestSqlRepository(db)

    __models_fake = ModelsFake()

    @pytest.fixture
    def get_titanic_test(self) -> List[Any]:
        return [self.__models_fake.get_fake_titanic_test(1),
                self.__models_fake.get_fake_titanic_test(2)]

    def test_get_all(self, monkeypatch, get_titanic_test):
        results = [get_titanic_test]
        self.mock_all_externals(monkeypatch, results)
        result = self.__test_sql_repository.get_all()

        assert result == get_titanic_test

    def test_get_by_id(self, monkeypatch, get_titanic_test):
        results = [get_titanic_test[0]]
        self.mock_all_externals(monkeypatch, results)
        result = self.__test_sql_repository.get_by_id(1)

        assert result == get_titanic_test[0]

    def test_create(self, monkeypatch, get_titanic_test):
        results = [get_titanic_test[0]]
        self.mock_all_externals(monkeypatch, results)
        result = self.__test_sql_repository.create(get_titanic_test[0])

        assert result == get_titanic_test[0]

    def test_bulk_load_data(self, monkeypatch, get_titanic_test):
        results = [get_titanic_test]
        self.mock_all_externals(monkeypatch, results)
        result = self.__test_sql_repository.bulk_load_data(get_titanic_test)

        assert result == get_titanic_test
