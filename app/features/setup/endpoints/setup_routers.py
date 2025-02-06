from fastapi import APIRouter, Depends
from app.core.security import get_current_user  # ✅ 修正: `get_current_user` を正しくインポート

# ✅ 認証が自動で適用されるルーター
setup_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    tags=["Setup"]  # ✅ Setup機能のタグを追加
)

# ステータス
from .setup_status import router as status_router
setup_router.include_router(status_router, prefix="/status", tags=["Setup - Status"])

# 性別
from .sex_selection import router as sex_router
setup_router.include_router(sex_router, prefix="/sex", tags=["Setup - Sex"])
