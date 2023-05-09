from typing import Any, List

import pytest
from database.database import database

from sqlalchemy.orm import Session
from etl.load.repository.titanic_train_sql_repository import TitanicTrainSqlRepository
from test.base_test import BaseTest
from test.fakes.models_fake import ModelsFake
from database.database import db


class TestSqlRepositoryTrain(BaseTest):
    __db = db
    __train_sql_repository = TitanicTrainSqlRepository(db)

    __models_fake = ModelsFake()

    @pytest.fixture
    def get_titanic_train(self) -> List[Any]:
        return [self.__models_fake.get_fake_titanic_train(1),
                self.__models_fake.get_fake_titanic_train(2)]

    def test_get_all(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train]
        self.mock_all_externals(monkeypatch, results)
        result = self.__train_sql_repository.get_all()

        assert result == get_titanic_train

    def test_get_by_id(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train[0]]
        self.mock_all_externals(monkeypatch, results)
        result = self.__train_sql_repository.get_by_id(1)

        assert result == get_titanic_train[0]

    def test_create(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train[0]]
        self.mock_all_externals(monkeypatch, results)
        result = self.__train_sql_repository.create(get_titanic_train[0])

        assert result == get_titanic_train[0]

    def test_bulk_load_data(self, monkeypatch, get_titanic_train):
        results = [get_titanic_train]
        self.mock_all_externals(monkeypatch, results)
        result = self.__train_sql_repository.bulk_load_data(get_titanic_train)

        assert result == get_titanic_train
