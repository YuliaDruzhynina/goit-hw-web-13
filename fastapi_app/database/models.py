from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fastapi_project.fastapi_app.database.db import Base, engine


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(150))
    phone_number = Column(String(20))
    email = Column(String(150), unique=True, index=True)
    birthday = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    contacts = relationship("Contact", back_populates="user")
    confirmed = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)
