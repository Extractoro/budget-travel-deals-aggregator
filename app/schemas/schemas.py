import re
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Literal, Union

from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic.v1 import validator


class UserSchema(BaseModel):
    user_id: int
    username: str

    model_config = {
        "from_attributes": True
    }


class RefreshRequest(BaseModel):
    email: EmailStr


class RyanairOneWayFareBody(BaseModel):
    departure: str = Field(..., min_length=3, max_length=3,
                           description="Departure airport IATA code")
    arrival: str = Field(..., min_length=3, max_length=3, description="Arrival airport IATA code")
    date_from: date = Field(..., description="Start date for fare search (YYYY-MM-DD)")
    date_to: date = Field(..., description="End date for fare search (YYYY-MM-DD)")
    currency: str = Field(
        'EUR',
        min_length=3,
        max_length=3,
        description="Currency code (e.g., USD, EUR)")

    @validator("date_to")
    def check_date_range(self, v, values):
        date_from = values.get("date_from")
        if date_from and v < date_from:
            raise ValueError("date_to must be greater than or equal to date_from")
        return v


class RyanairFlightsSearch(BaseModel):
    origin: str = Field(..., alias="originIata", min_length=3, max_length=3,
                        description="Origin airport IATA code")
    destination: str = Field(..., alias="destinationIata", min_length=3,
                             max_length=3, description="Destination airport IATA code")
    date_out: date = Field(..., alias="dateOut", description="Departure date (YYYY-MM-DD)")
    date_in: Optional[date] = Field(
        None,
        alias="dateIn",
        description="Return date (YYYY-MM-DD), optional")
    adults: int = Field(1, ge=1, le=6, description="Number of adult passengers (1-6)")
    teens: int = Field(0, ge=0, le=6, description="Number of teen passengers (0-6)")
    children: int = Field(0, ge=0, le=6, description="Number of child passengers (0-6)")
    infants: int = Field(0, ge=0, le=6, description="Number of infant passengers (0-6)")
    is_return: bool = Field(True, alias="isReturn", description="Whether it's a round-trip flight")
    # discount: int = Field(0, ge=0, description="Discount percentage, if applicable")
    # promo_code: Optional[str] = Field(
    # "", alias="promoCode", description="Promo code for discounts")
    # is_connected_flight: bool = Field(
    #     False,
    #     alias="isConnectedFlight",
    #     description="If the flight is a connected/multi-leg trip")

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
    children_ages: Optional[List[int]] = Field(
        default=None, description="List of children's ages (1–17)")

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


class HotelSortEnum(str, Enum):
    title = "title"
    price = "price"
    rating = "rating"
    address = "address"


class AirlineSortEnum(str, Enum):
    departure_time = "departure_time"
    price = "price"
    duration = "duration"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class FilteringParams(BaseModel):
    hotel_sort: Optional[HotelSortEnum] = None
    hotel_sort_order: SortOrder = SortOrder.asc
    airline_sort: Optional[AirlineSortEnum] = None
    airline_sort_order: SortOrder = SortOrder.asc


class AuthUserCredentials(BaseModel):
    username: str = Field(..., min_length=4)
    password: str = Field(..., min_length=8)

    @classmethod
    @field_validator("password")
    def password_complexity(cls, v):
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class SubscriptionRequest(BaseModel):
    task_id: str


class TaskResponse(BaseModel):
    task_id: str


class RyanairOneFareResult(BaseModel):
    departure: str
    arrival: str
    departureDate: datetime
    arrivalDate: datetime
    price: float
    currency: str


class RyanairOneFareTaskResult(BaseModel):
    task_id: str
    results: List[RyanairOneFareResult]


class RyanairFlightInfo(BaseModel):
    airline: str
    flight_number: str
    departure_time: str
    departure_city: str
    arrival_time: str
    arrival_city: str
    duration: str
    price: str


class RyanairSearchParams(BaseModel):
    adults: str
    teens: str
    children: str
    infants: str
    dateOut: str
    dateIn: str
    isConnectedFlight: str
    discount: str
    promoCode: str
    isReturn: str
    originIata: str
    destinationIata: str
    tpAdults: str
    tpTeens: str
    tpChildren: str
    tpInfants: str
    tpStartDate: str
    tpEndDate: str
    tpDiscount: str
    tpPromoCode: str
    tpOriginIata: str
    tpDestinationIata: str


class RyanairFlightResult(BaseModel):
    search_params: RyanairSearchParams
    url: str
    outbound: List[RyanairFlightInfo]
    inbound: List[RyanairFlightInfo]
    total_flights: int


class RyanairFlightTaskResult(BaseModel):
    task_id: str
    results: List[RyanairFlightResult]


class HotelResult(BaseModel):
    title: str
    address: Optional[str] = None
    distance: Optional[str] = None
    rating: Optional[float] = None
    amenities: List[str]
    old_price: Optional[float] = None
    current_price: Optional[float] = None
    taxes: Union[str, None] = None


class HotelTaskResult(BaseModel):
    task_id: str
    results: List[HotelResult]


class SubscriptionResult(BaseModel):
    detail: str


class FlightDifference(BaseModel):
    departure: str
    arrival: str
    departureDate: str
    price_old: str
    price_new: str
    price_diff: str
    currency: str


class HotelDifference(BaseModel):
    title: str
    price_old: str
    price_new: str
    price_diff: str


class FlightDiffWithChanges(BaseModel):
    type: Literal["oneway_flight", "flight"]
    differences: List[FlightDifference]
    has_changes: Literal[True]


class HotelDiffWithChanges(BaseModel):
    type: Literal["hotel"]
    differences: List[HotelDifference]
    has_changes: Literal[True]


class DiffNoChanges(BaseModel):
    type: Literal["oneway_flight", "flight", "hotel"]
    differences: str
    has_changes: Literal[False]


class SubscriptionDiffResponse(BaseModel):
    diff: Union[
        FlightDiffWithChanges,
        HotelDiffWithChanges,
        DiffNoChanges
    ]
