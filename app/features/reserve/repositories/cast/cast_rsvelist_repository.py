# 📂 app/features/reserve/repositories/cast/cast_rsvelist_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.models.resv_reservation import ResvReservation
from app.db.models.user import User
from app.db.models.point_details import PointDetailsCourse
from app.db.models.resv_status_detail import ResvStatusDetail
from app.db.models.resv_chat import ResvChat
from app.db.models.station import Station

def get_cast_reservations(db: Session, cast_id: int, limit: int, offset: int):
    latest_message_subquery = (
        select(
            ResvChat.reservation_id,
            func.max(ResvChat.created_at).label("last_message_time"),
            func.substr(ResvChat.message, 1, 5).label("last_message_preview")
        )
        .group_by(ResvChat.reservation_id)
        .subquery()
    )

    stmt = (
        select(
            ResvReservation.id.label("reservation_id"),
            ResvReservation.user_id,
            User.nick_name.label("user_name"),
            ResvStatusDetail.cast_label.label("status"), 
            ResvStatusDetail.status_key,
            ResvReservation.start_time,
            PointDetailsCourse.course_name,
            PointDetailsCourse.cost_points.label("course_price"),
            ResvReservation.traffic_fee,
            ResvStatusDetail.color_code,
            Station.name.label("location"),
            latest_message_subquery.c.last_message_time,
            latest_message_subquery.c.last_message_preview
        )
        .join(User, ResvReservation.user_id == User.id)
        .join(PointDetailsCourse, ResvReservation.course_id == PointDetailsCourse.id)
        .join(ResvStatusDetail, ResvReservation.status == ResvStatusDetail.status_key)
        .join(Station, ResvReservation.location == Station.id)
        .outerjoin(latest_message_subquery, ResvReservation.id == latest_message_subquery.c.reservation_id)
        .filter(ResvReservation.cast_id == cast_id)
        .order_by(ResvReservation.start_time.desc())
        .limit(limit)
        .offset(offset)
    )

    results = db.execute(stmt).mappings().all()
    return results

# ✅ これを追加！
def get_total_reservation_count(db: Session, cast_id: int):
    return db.query(ResvReservation).filter(ResvReservation.cast_id == cast_id).count()
