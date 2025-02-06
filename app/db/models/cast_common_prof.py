from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class CastCommonProf(Base):
    __tablename__ = "cast_common_prof"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cast_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)  # ✅ users.idと紐付け
    cast_type = Column(Enum('A', 'B'), nullable=False)  
    rank_id = Column(Integer, ForeignKey("cast_rank.id", ondelete="SET NULL"))
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    height = Column(Integer)
    bust = Column(Integer)
    cup = Column(String(255))
    waist = Column(Integer)
    hip = Column(Integer)
    birthplace = Column(String(255))
    blood_type = Column(String(255))
    hobby = Column(String(255))
    profile_image_url = Column(String(255))
    reservation_fee = Column(Integer)
    self_introduction = Column(String(255))
    job = Column(String(255))
    dispatch_prefecture = Column(String(255))
    support_area = Column(String(255))
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
