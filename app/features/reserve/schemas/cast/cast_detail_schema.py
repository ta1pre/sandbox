# 📂 app/features/reserve/schemas/cast/cast_detail_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CastReservationDetailResponse(BaseModel):
    reservation_id: int
    user_name: str
    course_name: str
    start_time: datetime
    end_time: datetime
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    traffic_fee: int
    reservation_fee: int
    total_points: int
    status: str
    reservation_note: Optional[str]
    cancel_reason: Optional[str]
