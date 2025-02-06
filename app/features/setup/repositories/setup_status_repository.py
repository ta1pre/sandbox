from sqlalchemy.orm import Session
from app.db.models.user import User
from typing import Optional


class SetupStatusRepository:
    def __init__(self, db: Session):
        self.db = db

    # ✅ 進捗状況の取得処理
    def get_setup_status(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return user.setup_status
        return None

    # ✅ 進捗状況の更新処理
    def update_setup_status(self, user_id: int, setup_status: str):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("ユーザーが存在しません")

        user.setup_status = setup_status  # ✅ 進捗状況の更新
        self.db.commit()
