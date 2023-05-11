from etl.load.model.titanic import Titanic
import datetime


class ModelsFake:
    @staticmethod
    def get_fake_titanic_train(id_: int = 1) -> Titanic:
        return Titanic(passenger_id=id_,
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
    def get_fake_titanic_test(id_: int = 1) -> Titanic:
        return Titanic(passenger_id=id_,
                       p_class=-1,
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
