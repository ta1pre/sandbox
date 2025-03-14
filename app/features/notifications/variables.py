# app/features/notifications/variables.py

from sqlalchemy.orm import Session
from app.db.models.resv_reservation import ResvReservation

def get_reservation_variables(db: Session, reservation_id: int) -> dict:
    """
    予約IDからDBの情報を取得し、テンプレートに渡す変数を作成
    """
    reservation = db.query(ResvReservation).filter(ResvReservation.id == reservation_id).first()

    if not reservation:
        print(f"❌ 予約ID {reservation_id} のデータが見つかりません")
        return {"location": "不明", "date": "不明", "time": "不明"}

    return {
        "location": reservation.location,
        "date": reservation.start_time.strftime("%Y-%m-%d"),
        "time": reservation.start_time.strftime("%H:%M"),
    }
