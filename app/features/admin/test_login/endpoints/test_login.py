# features/admin/testLogin/endpoints/test_login.py
from fastapi import APIRouter

router = APIRouter(
    tags=["Admin - テストログイン"]
)

@router.post("/login")
async def complete_status():
    """
    ✅ 認証付きのシンプルなAPI
    ✅ FastAPI側で正常に動作しているか確認するためのエンドポイント
    """
    return {"message": "OK"}
