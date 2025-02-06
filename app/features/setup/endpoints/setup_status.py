# ✅ setup_status.py - 進捗状況のみ管理
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db  # ✅ 元のパスに修正
from app.features.setup.repositories.setup_status_repository import SetupStatusRepository
from app.features.setup.schemas.status_schema import SetupStatusRequest, SetupStatusResponse  # ✅ スキーマを分割してインポート
from app.core.security import get_current_user  # ✅ 認証処理を追加

router = APIRouter()

# ✅ 進捗状況の取得エンドポイント（復元）
@router.get("/", response_model=SetupStatusResponse)
def get_setup_status(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # ✅ 自動的に認証されたuser_idを取得
):
    """
    現在のセットアップステータスを取得
    """
    status_repo = SetupStatusRepository(db)  # ✅ リポジトリ経由でDBアクセス
    setup_status = status_repo.get_setup_status(user_id)

    if setup_status is None:
        return {"user_id": user_id, "setup_status": "empty"}

    return {"user_id": user_id, "setup_status": setup_status}

# ✅ 進捗状況のみの更新エンドポイント（POST /update に変更）
@router.post("/update")
def update_setup_status(
    data: SetupStatusRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # ✅ 認証済みユーザーIDを取得
):
    try:
        status_repo = SetupStatusRepository(db)  # ✅ リポジトリ経由でDB更新
        status_repo.update_setup_status(user_id, data.setup_status)
        return {"status": "success", "message": "進捗状況を更新しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新に失敗しました: {str(e)}")
