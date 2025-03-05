from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.features.customer.search.service.search_service import fetch_cast_list
from app.features.customer.search.schemas.search_schema import SearchRequest  # ✅ スキーマをインポート
from app.features.customer.search.schemas.user_schema import UserPrefectureRequest  # ✅ スキーマをインポート
from app.features.customer.search.repositories.user_repository import get_user_prefecture

router = APIRouter()

@router.post("/")
def search_casts(request: SearchRequest, db: Session = Depends(get_db)):
    print(f"【バックエンド API 受信】 offset: {request.offset}, limit: {request.limit}, sort: {request.sort}, filters: {request.filters}")  # ✅ 確認
    filters = request.filters or {}
    return fetch_cast_list(request.limit, request.offset, request.sort, request.filters, db)  

@router.post("/user/prefecture")
def get_user_prefecture_endpoint(request: UserPrefectureRequest, db: Session = Depends(get_db)):
    """ユーザーの都道府県IDを取得"""
    user_id = request.user_id  # ✅ 明示的に `user_id` を取得
    prefecture = get_user_prefecture(db, user_id)  # ✅ 修正: `request.user_id` を正しく渡す
    
    if prefecture is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"prefecture": prefecture}