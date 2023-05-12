import datetime

import pytz
from sqlalchemy import Column, DateTime, Float, Integer, SmallInteger, String

from database.database import Base


class Titanic(Base):
    __tablename__ = "titanic"

    passenger_id = Column(Integer, primary_key=True)
    survived = Column(Integer, nullable=True)
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

    def __repr__(self):
        return f"Titanic(passenger_id='{self.passenger_id}', " \
               f"survived={self.survived}, " \
               f"p_class={self.p_class}, "\
               f"name={self.name}, " \
               f"sex={self.sex}, " \
               f"age={self.age}, " \
               f"sib_sp={self.sib_sp}, " \
               f"ticket={self.ticket}, " \
               f"fare={self.fare}, " \
               f"cabin={self.cabin}, "\
               f"embarked={self.embarked}, " \
               f"created_at='{self.created_at}')"
