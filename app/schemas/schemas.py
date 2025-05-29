from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class RyanairOneWayFareParams(BaseModel):
    departure: str
    arrival: str
    date_from: date
    date_to: date
    currency: str


class RyanairFlightsSearch(BaseModel):
    origin: str = Field('BER', alias="originIata", min_length=3, max_length=3)
    destination: str = Field('BCN', alias="destinationIata", min_length=3, max_length=3)
    date_out: date = Field('2025-06-10', alias="dateOut")
    date_in: Optional[date] = Field('2025-06-21', alias="dateIn")
    adults: int = Field(1, ge=1, le=6)
    teens: int = Field(0, ge=0, le=6)
    children: int = Field(0, ge=0, le=6)
    infants: int = Field(0, ge=0, le=6)
    is_return: bool = Field(True, alias="isReturn")
    discount: int = Field(0, ge=0)
    promo_code: Optional[str] = Field('', alias="promoCode")
    is_connected_flight: bool = Field(False, alias="isConnectedFlight")
