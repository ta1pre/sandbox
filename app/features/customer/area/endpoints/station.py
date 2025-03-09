from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.station_schema import LocationRequest, StationResponse, StationRegisterRequest, StationCurrentRequest
from ..service.station_service import get_nearest_stations, register_station_for_user, fetch_current_station
from app.db.session import get_db
from app.core.security import get_current_user
from typing import List

router = APIRouter()

@router.post("/station/nearest", response_model=List[StationResponse])
def nearest_stations(request: LocationRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """現在地から近い駅を取得"""

    # ✅ userがint（ユーザーID）の場合
    user_id = user if isinstance(user, int) else user.id

    return get_nearest_stations(db, user_id, request.lat, request.lon)

@router.post("/station/register")
def register_nearest_station(request: StationRegisterRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """最寄り駅を登録"""

    # ✅ userがint（ユーザーID）の場合
    user_id = user if isinstance(user, int) else user.id

    return register_station_for_user(db, user_id, request.station)

@router.post("/station/current", response_model=StationResponse)
def get_current_station(request: StationCurrentRequest, db: Session = Depends(get_db)):
    """現在の最寄り駅を取得（POST）"""
    return fetch_current_station(db, request.user_id)
