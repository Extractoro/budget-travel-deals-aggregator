from app.api.hotels import router as hotels_router
from app.api.flights import router as flights_router
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.subscription import router as subscription_router
from fastapi import FastAPI


app = FastAPI()
app.include_router(router=auth_router, prefix='/auth', tags=['Authentication'])
app.include_router(router=profile_router, prefix='/profile', tags=['Profile'])
app.include_router(router=flights_router, prefix='/flights')
app.include_router(router=hotels_router, prefix='/hotels')
app.include_router(router=subscription_router, prefix='/subscription', tags=['Subscription'])
