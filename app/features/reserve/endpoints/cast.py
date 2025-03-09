# app/features/reserve/endpoints/cast.py

from fastapi import APIRouter

cast_router = APIRouter()

@cast_router.post("/test")
def test_cast():
    return {"message": "Cast endpoint is working"}