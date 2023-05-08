from typing import List

from sqlalchemy.orm import Session

from etl.load.model.titanic_train import TitanicTrain
from etl.load.repository.titanic_repository import TitanicRepository
from loguru import logger


class TitanicTrainSqlRepository(TitanicRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[TitanicTrain]:
        return self.db.query(TitanicTrain).all()

    def get_by_id(self, passenger_id: int) -> TitanicTrain:
        return self.db.query(TitanicTrain).get(passenger_id)

    def create(self, titanic_train: TitanicTrain) -> TitanicTrain:
        self.db.add(titanic_train)
        self.db.commit()
        self.db.refresh(titanic_train)
        return titanic_train

    def update(self, titanic_train: TitanicTrain) -> TitanicTrain:
        self.db.commit()
        self.db.refresh(titanic_train)
        return titanic_train

    def delete(self, titanic_train: TitanicTrain) -> None:
        self.db.delete(titanic_train)
        self.db.commit()

    def bulk_load_data(self, data: List):
        titanic_train_data = [TitanicTrain(passenger_id=int(row[0]),
                                           survived=int(row[1]),
                                           p_class=int(row[2]),
                                           name=row[3],
                                           sex=row[4],
                                           age=float(row[5]) if row[5] != '' else None,
                                           sib_sp=int(row[6]),
                                           parch=int(row[7]),
                                           ticket=row[8],
                                           fare=float(row[9]),
                                           cabin=row[10] if row[10] != '' else 'NaN',
                                           embarked=row[11] if row[11] != '' else 'C') for row in data]

        try:
            self.db.bulk_save_objects(titanic_train_data)
        except Exception as ex:
            self.db.rollback()
            logger.error(ex.__str__())
