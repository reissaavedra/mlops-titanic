from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from configuration.settings import settings as s


class Database:
    __engine = None

    def get_engine(self):
        if self.__engine is None:
            url = f"postgresql://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}/{s.DB_NAME}"
            self.__engine = create_engine(url, pool_size=20, echo=False, pool_pre_ping=True)
        return self.__engine

    def get_session(self) -> Session:
        engine = self.get_engine()
        session = sessionmaker(bind=engine, autocommit=True)
        return session()


database = Database()
engine = database.get_engine()
db = database.get_session()
Base = declarative_base()
