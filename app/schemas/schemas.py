from pydantic import BaseModel
from datetime import date


class FlightsGetParams(BaseModel):
    departure: str
    arrival: str
    date_from: date
    date_to: date
    currency: str
