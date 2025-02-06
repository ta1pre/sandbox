from pydantic import BaseModel, Field


class SetupStatusRequest(BaseModel):
    setup_status: str = Field(..., description="進捗状況")

class SetupStatusResponse(BaseModel):
    user_id: int
    setup_status: str
