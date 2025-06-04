from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class DataResults(Base):
    __tablename__ = "data_results"

    task_id = Column(String, primary_key=True, index=True)
    data = Column(JSON)


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    task_id = Column(String, ForeignKey('data_results.task_id'), primary_key=True)
