from typing import List

from loguru import logger
from sqlalchemy.orm import Session

from etl.load.model.titanic_test import TitanicTest
from etl.load.repository.titanic_repository import TitanicRepository


class TitanicTestSqlRepository(TitanicRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[TitanicTest]:
        return self.db.query(TitanicTest).all()

    def get_by_id(self, id: int) -> TitanicTest:
        return self.db.query(TitanicTest).get(id)

    def create(self, titanic_test: TitanicTest) -> TitanicTest:
        self.db.add(titanic_test)
        self.db.commit()
        self.db.refresh(titanic_test)
        return titanic_test

    def update(self, titanic_test: TitanicTest) -> TitanicTest:
        self.db.commit()
        self.db.refresh(titanic_test)
        return titanic_test

    def delete(self, titanic_test: TitanicTest) -> None:
        self.db.delete(titanic_test)
        self.db.commit()

    def bulk_load_data(self, data: List):
        titanic_test_data = [TitanicTest(passenger_id=int(row[0]),
                                         p_class=int(row[1]),
                                         name=row[2],
                                         sex=row[3],
                                         age=float(row[4]) if row[4] != '' else None,
                                         sib_sp=int(row[5]),
                                         parch=int(row[6]),
                                         ticket=row[7],
                                         fare=float(row[8]) if row[8] != '' else 100.0,
                                         cabin=row[10] if row[10] != '' else 'NaN',
                                         embarked=row[10]) for row in data]

        try:
            self.db.bulk_save_objects(titanic_test_data)
            return titanic_test_data
        except Exception as ex:
            self.db.rollback()
            logger.error(ex.__str__())
