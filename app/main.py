from app.api.hotels import router as hotels_router
from app.api.flights import router as flights_router
from app.api.auth import router as auth_router
from fastapi import FastAPI


app = FastAPI()
app.include_router(router=auth_router, prefix='/auth')
app.include_router(router=flights_router, prefix='/flights')
app.include_router(router=hotels_router, prefix='/hotels')
