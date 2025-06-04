from app.api.hotels import router as hotels_router
from app.api.flights import router as flights_router
from fastapi import FastAPI


app = FastAPI()
app.include_router(router=flights_router, prefix='/flights')
app.include_router(router=hotels_router, prefix='/hotels')
