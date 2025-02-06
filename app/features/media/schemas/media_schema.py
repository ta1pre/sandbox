# ✅ media_schema.py - リクエスト・レスポンススキーマ
from pydantic import BaseModel, Field

class MediaUploadRequest(BaseModel):
    file_name: str = Field(..., example="profile_image.jpg")
    file_type: str = Field(..., example="image/jpeg")
    target_type: str = Field(..., example="profile_a")
    target_id: int = Field(..., example=1)

class MediaUploadResponse(BaseModel):
    presigned_url: str = Field(..., example="https://s3.amazonaws.com/.../profile_image.jpg")

class MediaRegisterRequest(BaseModel):
    file_url: str = Field(..., example="https://s3.amazonaws.com/.../profile_image.jpg")
    file_type: str = Field(..., example="image/jpeg")
    target_type: str = Field(..., example="profile_a")
    target_id: int = Field(..., example=1)
    order_index: int = Field(..., example=0)

class MediaDeleteResponse(BaseModel):
    status: str = Field(..., example="success")
    message: str = Field(..., example="メディアファイルが削除されました。")