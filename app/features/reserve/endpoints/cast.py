# app/features/reserve/endpoints/cast.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db


cast_router = APIRouter()

@cast_router.post("/test")
def test_cast():
    return {"message": "Cast endpoint is working"}

# ✅ 新規追加：キャスト用予約一覧取得API（ページネーション対応）
from app.features.reserve.service.cast.cast_rsvelist_service import get_cast_reservation_list
from app.features.reserve.schemas.cast.cast_rsvelist_schema import CastRsveListResponse

@cast_router.post("/rsvelist", response_model=CastRsveListResponse)
def cast_reservation_list(request: dict, db: Session = Depends(get_db)):
    cast_id = request.get("cast_id")
    page = request.get("page", 1)
    limit = request.get("limit", 10)

    if not cast_id:
        raise HTTPException(status_code=400, detail="cast_id は必須です")

    response_obj = get_cast_reservation_list(db, cast_id, page, limit)
    return response_obj


# ✅ 個別予約ページ
from app.features.reserve.service.cast.cast_detail_service import get_reservation_detail
from app.features.reserve.schemas.cast.cast_detail_schema import CastReservationDetailResponse
@cast_router.post("/detail", response_model=CastReservationDetailResponse)
def fetch_reservation_detail(request: dict, db: Session = Depends(get_db)):
    reservation_id = request.get("reservation_id")
    cast_id = request.get("cast_id")

    if not reservation_id or not cast_id:
        raise HTTPException(status_code=400, detail="reservation_id, cast_id は必須です")

    return get_reservation_detail(db, reservation_id, cast_id)


# ✅ 表示用オプションの取得
# スキーマ & サービスインポート
from app.features.reserve.schemas.cast.cast_options_schema import (
    CastOptionRequest,
    CastOptionResponse
)
from app.features.reserve.service.cast.cast_options_service import get_cast_options

@cast_router.post("/options", response_model=CastOptionResponse)
def fetch_cast_options(request: CastOptionRequest, db: Session = Depends(get_db)):
    """
    キャストが対応できるオプション一覧 & 予約に紐づいているオプション一覧を取得
    """
    return get_cast_options(db, request)

