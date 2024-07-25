from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from sqlalchemy.orm import DeclarativeBase


SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:567234@localhost:5432/restapp_hw13"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True
    pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
