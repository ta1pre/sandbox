from fastapi import APIRouter, Depends, HTTPException, Security, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone 
from app.core.security import create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
from app.db.session import get_db
from app.features.account.repositories.account_repository import AccountRepository

router = APIRouter()
security = HTTPBearer()

# ✅ 環境変数から `Secure` の設定を動的に変更
import os
IS_PRODUCTION = os.getenv("ENV") == "production"

# ✅ リクエストモデル定義
class TokenRequest(BaseModel):
    user_id: int

# 📌 JWTトークン生成（ログイン時）
@router.post("/token")
def generate_jwt_token(response: Response, request: TokenRequest, db: Session = Depends(get_db)):
    """
    ユーザーIDを指定してJWTトークンを生成し、`refresh_token` を `HttpOnly Cookie` に保存
    """
    user_repo = AccountRepository(db)
    user = user_repo.get_user_by_id(request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token(user.id, user.type, user.affi_type)
    refresh_token = create_refresh_token(user.id)

    # ✅ `refresh_token` を `HttpOnly Cookie` に保存
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=IS_PRODUCTION,  # ✅ 本番環境なら `Secure=True`
        samesite="Lax",
        max_age=30 * 24 * 60 * 60  # 30日間
    )

    return {"access_token": access_token, "token_type": "bearer"}

# ✅ `access_token` を検証（通常のAPIリクエストで呼ばれる）
@router.get("/verify")
def verify_jwt_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    `access_token` の有効性を検証する
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="No valid token provided")

    token = credentials.credentials
    try:
        token_data = verify_access_token(token)
        user_id = token_data.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload: user_id is missing")

        user_repo = AccountRepository(db)
        user = user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # ✅ `Set-Cookie` を明示的に設定（CORSエラー回避）
        response = Response()
        response.set_cookie(
            key="test_cookie",
            value="test_value",
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return {
            "user_id": user.id,
            "user_type": user.type,
            "affi_type": user.affi_type,
            "message": "Token is valid"
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token Error: {str(e)}")


# ✅ `refresh_token` を `HttpOnly Cookie` から取得し、新しい `access_token` を発行
@router.post("/refresh")
def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    `refresh_token` を `HttpOnly Cookie` から取得し、新しい `access_token` を発行
    """
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No valid refresh token provided")

    try:
        token_data = verify_refresh_token(refresh_token)
        user_id = token_data.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token payload: user_id is missing")

        user_repo = AccountRepository(db)
        user = user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # ✅ `access_token` を発行
        new_access_token = create_access_token(user.id, user.type, user.affi_type)
        new_refresh_token = create_refresh_token(user.id)

        # ✅ `refresh_token` を `HttpOnly Cookie` に更新
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=IS_PRODUCTION,  # ✅ 本番環境では `Secure=True`
            samesite="Lax",
            max_age=30 * 24 * 60 * 60  # 30日間
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Refresh Token Error: {str(e)}")


#refresh_token の有効期限を検証
@router.get("/refresh_token_expiration")
def get_refresh_token_expiration(request: Request):
    """
    クライアントの `refresh_token` の有効期限を返す
    """
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No valid refresh token provided")

    try:
        token_data = verify_refresh_token(refresh_token)
        exp_timestamp = token_data.get("exp")

        if not exp_timestamp:
            raise HTTPException(status_code=401, detail="Invalid token payload: exp is missing")

        # Unixタイムスタンプを人間が読める形に変換
        expiration_datetime = datetime.fromtimestamp(exp_timestamp, timezone.utc)
        return {"expiration": expiration_datetime.isoformat()}

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Refresh Token Error: {str(e)}")