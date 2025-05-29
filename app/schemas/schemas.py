from datetime import date
from typing import Optional, List, Literal

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class RyanairOneWayFareParams(BaseModel):
    departure: str = Field(..., min_length=3, max_length=3, description="Departure airport IATA code")
    arrival: str = Field(..., min_length=3, max_length=3, description="Arrival airport IATA code")
    date_from: date = Field(..., description="Start date for fare search (YYYY-MM-DD)")
    date_to: date = Field(..., description="End date for fare search (YYYY-MM-DD)")
    currency: str = Field('EUR', min_length=3, max_length=3, description="Currency code (e.g., USD, EUR)")

    @validator("date_to")
    def check_date_range(self, v, values):
        date_from = values.get("date_from")
        if date_from and v < date_from:
            raise ValueError("date_to must be greater than or equal to date_from")
        return v


class RyanairFlightsSearch(BaseModel):
    origin: str = Field(..., alias="originIata", min_length=3, max_length=3, description="Origin airport IATA code")
    destination: str = Field(..., alias="destinationIata", min_length=3, max_length=3, description="Destination airport IATA code")
    date_out: date = Field(..., alias="dateOut", description="Departure date (YYYY-MM-DD)")
    date_in: Optional[date] = Field(None, alias="dateIn", description="Return date (YYYY-MM-DD), optional")
    adults: int = Field(1, ge=1, le=6, description="Number of adult passengers (1-6)")
    teens: int = Field(0, ge=0, le=6, description="Number of teen passengers (0-6)")
    children: int = Field(0, ge=0, le=6, description="Number of child passengers (0-6)")
    infants: int = Field(0, ge=0, le=6, description="Number of infant passengers (0-6)")
    is_return: bool = Field(True, alias="isReturn", description="Whether it's a round-trip flight")
    discount: int = Field(0, ge=0, description="Discount percentage, if applicable")
    promo_code: Optional[str] = Field("", alias="promoCode", description="Promo code for discounts")
    is_connected_flight: bool = Field(False, alias="isConnectedFlight", description="If the flight is a connected/multi-leg trip")

    @validator("date_in")
    def validate_return_date(self, return_date, values):
        date_out = values.get("date_out")
        if return_date and date_out and return_date <= date_out:
            raise ValueError("Return date must be after the departure date")
        return return_date


class HotelsSearch(BaseModel):
    destination: str = Field(..., description="City or region to search hotels in")
    checkin: date = Field(..., description="Check-in date (format YYYY-MM-DD)")
    checkout: date = Field(..., description="Check-out date (format YYYY-MM-DD)")
    adults: int = Field(..., gt=0, description="Number of adults (must be at least 1)")
    rooms: int = Field(..., gt=0, description="Number of rooms (must be at least 1)")
    children_ages: Optional[List[int]] = Field(default=None, description="List of children's ages (1–17)")
    sort: Literal["RECOMMENDED", "PRICE_LOW_TO_HIGH", "PRICE_HIGH_TO_LOW"] = Field(
        "RECOMMENDED", description="Sorting option for hotel results"
    )

    @validator("children_ages", each_item=True)
    def validate_child_age(self, v):
        if not (1 <= v <= 17):
            raise ValueError("Each child's age must be between 1 and 17")
        return v

    @validator("checkout")
    def validate_dates(self, checkout_date, values):
        checkin_date = values.get("checkin")
        if checkin_date and checkout_date <= checkin_date:
            raise ValueError("Check-out date must be after check-in date")
        return checkout_date
