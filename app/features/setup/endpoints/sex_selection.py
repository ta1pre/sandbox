# ✅ sex_selection.py - 性別とユーザータイプの更新および取得エンドポイント
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.features.setup.repositories.setup_sex_repository import SetupSexRepository
from app.features.setup.schemas.sex_schema import SexSelectionRequest
from app.core.security import get_current_user

router = APIRouter()

# ✅ 性別とユーザータイプの取得エンドポイント
@router.get("/")
def get_sex(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    性別とユーザータイプの取得
    """
    sex_repo = SetupSexRepository(db)
    user_info = sex_repo.get_user_sex(user_id=user_id)

    if user_info is None:
        raise HTTPException(status_code=404, detail="ユーザー情報が見つかりません")

    return {
        "user_id": user_id,
        "sex": user_info.sex,
        "user_type": user_info.type
    }

# ✅ 性別とユーザータイプの更新エンドポイント
@router.post("/")
def select_sex(
    request: SexSelectionRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    性別とユーザータイプの更新
    """
    sex_repo = SetupSexRepository(db)
    success = sex_repo.update_user_sex(user_id=user_id, sex=request.sex, user_type=request.user_type)

    if not success:
        raise HTTPException(status_code=400, detail="性別とユーザータイプの更新に失敗しました")

    return {"status": "success", "message": "性別とユーザータイプを更新しました"}