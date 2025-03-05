from sqlalchemy import Column, Integer, ForeignKey, String, Enum, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# ✅ キャストが提供するオプション
class PointOptionMap(Base):
    __tablename__ = "pnt_option_map"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cast_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ キャストID
    option_id = Column(Integer, nullable=False)  # ✅ オプションID
    is_active = Column(Boolean, default=True)  # ✅ オプションの有効/無効
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    cast = relationship("User", back_populates="option_map")


# ✅ ポイントルール定義
class PointDetailsRules(Base):
    __tablename__ = "pnt_details_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(255), nullable=False)  # ✅ ルール名
    rule_description = Column(String(255), nullable=True)  # ✅ ルールの説明
    point_type = Column(Enum("regular", "bonus", name="point_type_enum"), nullable=False)  # ✅ ポイント種別
    service_type = Column(Enum("service", "event", "coupon", name="service_type_enum"), nullable=False)  # ✅ サービス種別
    point_value = Column(Float, nullable=False)  # ✅ 獲得/消費ポイント
    is_addition = Column(Boolean, nullable=False, default=True)  # ✅ 追加(True) or 消費(False)
    created_at = Column(DateTime, server_default=func.now())

    
# ✅ コースのオプション
class PointDetailsOption(Base):
    __tablename__ = "pnt_details_option"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("pnt_details_course.id"), nullable=False)  # ✅ コースID
    option_name = Column(String(255), nullable=False)  # ✅ オプション名
    price = Column(Integer, nullable=False, default=0)  # ✅ オプション価格
    description = Column(String(255), nullable=True)  # ✅ オプションの説明
    created_at = Column(DateTime, server_default=func.now())

    course = relationship("PointDetailsCourse", back_populates="options")


# ✅ コース詳細
class PointDetailsCourse(Base):
    __tablename__ = "pnt_details_course"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_type = Column(Integer, nullable=False)  # ✅ コース種別
    course_name = Column(String(255), nullable=False)  # ✅ コース名
    description = Column(String(255), nullable=True)  # ✅ コース説明
    duration_minutes = Column(Integer, nullable=False)  # ✅ 時間（分）
    cost_points = Column(Integer, nullable=False)  # ✅ 必要ポイント
    cast_reward_points = Column(Integer, nullable=False)  # ✅ キャスト報酬ポイント
    is_active = Column(Boolean, default=True)  # ✅ コースの有効/無効
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    options = relationship("PointDetailsOption", back_populates="course")
