# 📂 app/features/reserve/service/cast/cast_detail_service.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.resv_reservation import ResvReservation
from app.db.models.user import User
from app.db.models.point_details import PointDetailsCourse
from fastapi import HTTPException

def get_reservation_detail(db: Session, reservation_id: int, cast_id: int):
    stmt = (
        select(
            ResvReservation.id.label("reservation_id"),
            User.nick_name.label("user_name"),
            PointDetailsCourse.course_name,
            ResvReservation.start_time,
            ResvReservation.end_time,
            ResvReservation.location,
            ResvReservation.latitude,
            ResvReservation.longitude,
            ResvReservation.traffic_fee,
            ResvReservation.reservation_fee,
            ResvReservation.total_points,
            ResvReservation.status,
            ResvReservation.reservation_note,
            ResvReservation.cancel_reason
        )
        .join(User, ResvReservation.user_id == User.id)
        .join(PointDetailsCourse, ResvReservation.course_id == PointDetailsCourse.id)
        .where(ResvReservation.id == reservation_id, ResvReservation.cast_id == cast_id)
    )

    reservation = db.execute(stmt).mappings().first()

    if not reservation:
        raise HTTPException(status_code=404, detail="予約が見つかりません")

    return reservation
