from typing import List

from loguru import logger
from sqlalchemy.orm import Session

from etl.load.model.titanic import Titanic
from etl.load.repository.titanic_repository import TitanicRepository


class TitanicSqlRepository(TitanicRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Titanic]:
        return self.db.query(Titanic).all()

    def get_by_id(self, passenger_id: int) -> Titanic:
        return self.db.query(Titanic).get(passenger_id)

    def create(self, titanic: Titanic) -> Titanic:
        self.db.add(titanic)
        self.db.commit()
        self.db.refresh(titanic)
        return titanic

    def update(self, titanic: Titanic) -> Titanic:
        self.db.commit()
        self.db.refresh(titanic)
        return titanic

    def delete(self, titanic: Titanic) -> None:
        self.db.delete(titanic)
        self.db.commit()

    def bulk_load_data(self, data: List[Titanic]) -> List:
        try:
            self.db.bulk_save_objects(data)
            return data
        except Exception as ex:
            self.db.rollback()
            logger.error(ex.__str__())
        return []
