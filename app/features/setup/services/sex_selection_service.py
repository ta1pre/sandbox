# app/features/setup/services/sex_selection_service.py

from sqlalchemy.orm import Session
from app.features.setup.repositories.setup_repository import get_user_sex_from_db, save_user_sex

def get_user_sex(db: Session, user_id: int) -> str:
    """
    ユーザーの性別を取得
    """
    return get_user_sex_from_db(db, user_id)

def set_user_sex(db: Session, user_id: int, sex: str) -> str:
    """
    ユーザーの性別を登録・更新
    """
    return save_user_sex(db, user_id, sex)
