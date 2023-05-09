import datetime

from etl.load.model.titanic_test import TitanicTest
from etl.load.model.titanic_train import TitanicTrain


class ModelsFake:
    @staticmethod
    def get_fake_titanic_train(id_: int = 1) -> TitanicTrain:
        return TitanicTrain(passenger_id=id_,
                            survived=1,
                            p_class=1,
                            name='test_name',
                            sex='male',
                            age=18,
                            sib_sp=1,
                            parch=1,
                            ticket='test',
                            fare=500.0,
                            cabin='NaN',
                            embarked='C',
                            created_at=datetime.datetime.now())

    @staticmethod
    def get_fake_titanic_test(id_: int = 1) -> TitanicTest:
        return TitanicTest(passenger_id=id_,
                           p_class=1,
                           name='test_name',
                           sex='male',
                           age=18,
                           sib_sp=1,
                           parch=1,
                           ticket='test',
                           fare=500.0,
                           cabin='NaN',
                           embarked='C',
                           created_at=datetime.datetime.now())
