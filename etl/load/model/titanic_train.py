import datetime

import pytz
from sqlalchemy import Column, Integer, SmallInteger, String, Float, DateTime
from database.database import Base


class TitanicTrain(Base):
    __tablename__ = "titanic_train"

    passenger_id = Column(Integer, primary_key=True)
    survived = Column(Integer, nullable=False)
    p_class = Column(SmallInteger)
    name = Column(String(250))
    sex = Column(String(20))
    age = Column(Float)
    sib_sp = Column(SmallInteger)
    parch = Column(SmallInteger)
    ticket = Column(String(50))
    fare = Column(Float)
    cabin = Column(String(20))
    embarked = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.now(pytz.timezone('America/New_York')))
