from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.features.media.services.media_service import generate_presigned_url, delete_media_file
from app.features.media.repositories.media_repository import save_media_info, delete_media_info
from app.features.media.schemas.media_schema import MediaUploadRequest, MediaUploadResponse, MediaRegisterRequest, MediaDeleteResponse

router = APIRouter()

# ✅ 署名付きURL発行エンドポイント
@router.post("/generate-url", response_model=MediaUploadResponse)
def create_presigned_url(
    request: MediaUploadRequest,
    current_user: int = Depends(get_current_user)
):
    try:
        presigned_url = generate_presigned_url(
            file_name=request.file_name,
            file_type=request.file_type,
            target_type=request.target_type,
            target_id=request.target_id
        )
        return {"presigned_url": presigned_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 URLの生成に失敗しました: {str(e)}")

# ✅ URL登録エンドポイント
@router.post("/register")
def register_uploaded_file(
    request: MediaRegisterRequest,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        save_media_info(
            file_url=request.file_url,
            file_type=request.file_type,
            target_type=request.target_type,
            target_id=request.target_id,
            order_index=request.order_index,
            db=db
        )
        return {"status": "success", "message": "メディアファイルが登録されました。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"メディアファイルの登録に失敗しました: {str(e)}")

# ✅ メディアファイル削除エンドポイント（修正版）
@router.delete("/delete/{media_id}", response_model=MediaDeleteResponse)
def delete_media_file_api(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        # ✅ 先にS3削除
        print(f"[DEBUG] S3削除開始: media_id={media_id}")
        delete_media_file(media_id, db)

        # ✅ S3削除後にDB削除
        print(f"[DEBUG] DB削除開始: media_id={media_id}")
        media = delete_media_info(media_id, db)  # ✅ 正しくDB削除
        if not media:
            raise HTTPException(status_code=404, detail="対象のメディアファイルが見つかりません")

        print(f"[DEBUG] DB削除成功: media_id={media_id}")
        return {"status": "success", "message": "メディアファイルとS3ファイルが削除されました。"}
    except HTTPException as http_err:
        print(f"[ERROR] HTTPエラー: {http_err.detail}")
        raise http_err
    except Exception as e:
        print(f"[ERROR] 予期しないエラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"メディアファイルの削除に失敗しました: {str(e)}")
