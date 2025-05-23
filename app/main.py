import uvicorn
from fastapi import FastAPI
from app.api.test import router as test_router

app = FastAPI()
app.include_router(router=test_router, prefix='/test', tags=['Testing'])