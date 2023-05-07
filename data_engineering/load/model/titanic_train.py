from sqlalchemy import Column, Integer, Boolean, SmallInteger, String, Float
from database.database import Base


class TitanicTrain(Base):
    __tablename__ = "titanic_train"

    passenger_id = Column(Integer, primary_key=True)
    survived = Column(Boolean, nullable=False)
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
