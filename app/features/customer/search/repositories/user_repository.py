# src/app/features/customer/search/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.db.models.user import User

def get_user_prefecture(db: Session, user_id: int):
    """ユーザーの都道府県IDを取得"""
    user = db.query(User.prefectures).filter(User.id == user_id).first()  # ✅ `User.prefecture` → `User.prefectures` に修正
    return user.prefectures if user else None  # ✅ 修正
