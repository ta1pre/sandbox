# app/features/reserve/endpoints/common.py

from fastapi import APIRouter

common_router = APIRouter()

@common_router.post("/test")
def test_common():
    return {"message": "Common endpoint is working"}