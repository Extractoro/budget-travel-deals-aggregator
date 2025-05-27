from fastapi import FastAPI
from app.api.flights import router as flights_router

app = FastAPI()
app.include_router(router=flights_router, prefix='/flights', tags=['Flights'])
