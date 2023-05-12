from test.base_test import BaseTest
from test.fakes.models_fake import ModelsFake
from typing import Any, List

import pytest

from database.database import db
from etl.load.model.titanic import Titanic
from etl.load.repository.titanic_sql_repository import TitanicSqlRepository


class TestSqlRepository(BaseTest):
    __db = db
    __titanic_sql_repository = TitanicSqlRepository(db)

    __models_fake = ModelsFake()

    @pytest.fixture
    def get_titanic_train(self) -> List[Titanic]:
        return [self.__models_fake.get_fake_titanic_train(1),
                self.__models_fake.get_fake_titanic_train(2)]

    @pytest.fixture
    def get_titanic_test(self) -> List[Titanic]:
        return [self.__models_fake.get_fake_titanic_test(1),
                self.__models_fake.get_fake_titanic_test(2)]

    def test_get_all(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train]
        self.mock_all_externals(monkeypatch, results)
        result = self.__titanic_sql_repository.get_all()

        assert result == get_titanic_train

    def test_get_by_id(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train[0]]
        self.mock_all_externals(monkeypatch, results)
        result = self.__titanic_sql_repository.get_by_id(1)

        assert result == get_titanic_train[0]

    def test_create(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train[0]]
        self.mock_all_externals(monkeypatch, results)
        result = self.__titanic_sql_repository.create(get_titanic_train[0])

        assert result == get_titanic_train[0]

    def test_bulk_load_data(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train]
        self.mock_all_externals(monkeypatch, results)
        result = self.__titanic_sql_repository.bulk_load_data(get_titanic_train)

        assert result == get_titanic_train
