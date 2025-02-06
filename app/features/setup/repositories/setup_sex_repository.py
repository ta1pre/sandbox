# ✅ setup_sex_repository.py - 性別とユーザータイプの取得および更新処理
from sqlalchemy.orm import Session
from app.db.models.user import User  # ✅ 正しいパスに修正

class SetupSexRepository:
    def __init__(self, db: Session):
        self.db = db

    # ✅ 性別とユーザータイプの取得処理
    def get_user_sex(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    # ✅ 性別とユーザータイプの更新処理
    def update_user_sex(self, user_id: int, sex: str, user_type: str):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        user.sex = sex
        user.type = user_type
        self.db.commit()
        return True
