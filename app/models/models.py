from sqlalchemy import Column, Integer, String, Float

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    departure = Column(String)
    arrival = Column(String)
    departureDate = Column(String)
    arrivalDate = Column(String)
    price = Column(Float)
    currency = Column(String)