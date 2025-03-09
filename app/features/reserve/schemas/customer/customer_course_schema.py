from pydantic import BaseModel

class CustomerCourseResponse(BaseModel):
    course_name: str
    duration: int  # ✅ `duration_minutes` に対応
    cost: int  # ✅ `cost_points` に対応

    class Config:
        orm_mode = True  # ✅ SQLAlchemyモデルとの互換性を確保
