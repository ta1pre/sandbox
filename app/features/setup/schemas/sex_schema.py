from pydantic import BaseModel, Field

# ✅ 性別とユーザータイプの更新リクエストスキーマ
class SexSelectionRequest(BaseModel):
    sex: str = Field(..., example="male", description="性別: male or female")
    user_type: str = Field(..., example="customer", description="ユーザータイプ: customer or cast")
