import enum

from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Enum as SqlEnum, DateTime, func
from app.database import Base


class DataTypeEnum(enum.Enum):
    HOTEL = "hotel"
    FLIGHT = "flight"
    ONEWAY_FLIGHT = "oneway_flight"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DataResults(Base):
    __tablename__ = "data_results"

    task_id = Column(String, primary_key=True, index=True)
    data_type = Column(SqlEnum(DataTypeEnum), nullable=False)
    params = Column(JSON, nullable=False)
    data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    task_id = Column(String, ForeignKey('data_results.task_id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
