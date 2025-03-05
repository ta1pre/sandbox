from sqlalchemy import Column, Integer, ForeignKey, String, Enum, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# ✅ ユーザーのポイント残高管理
class PointBalance(Base):
    __tablename__ = "pnt_user_point_balances"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)  # ✅ PRIMARY KEY（ユーザーID）
    regular_point_balance = Column(Integer, nullable=False, default=0)  # ✅ 通常ポイント
    bonus_point_balance = Column(Integer, nullable=False, default=0)  # ✅ ボーナスポイント
    total_point_balance = Column(Integer, nullable=False, default=0)  # ✅ 合計ポイント
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())  # ✅ 最終更新時刻

    # ✅ ユーザーとのリレーション（オプション）
    user = relationship("User", back_populates="point_balance")


# ✅ ポイント取引履歴
class PointTransaction(Base):
    __tablename__ = "pnt_point_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 取引ID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ ユーザーID
    related_id = Column(Integer, nullable=True)  # ✅ 関連ID（予約IDなど）
    related_table = Column(Enum("reservation", "event", "coupon", "purchase", "manual", name="related_table_enum"), nullable=True)  # ✅ 関連テーブル種別
    transaction_type = Column(Enum("deposit", "refund", "release", "event_bonus", "manual_adjustment", "purchase", name="transaction_type_enum"), nullable=False)  # ✅ 取引タイプ
    point_change = Column(Integer, nullable=False)  # ✅ 変更ポイント数
    point_source = Column(Enum("regular", "bonus", name="point_source_enum"), nullable=False, default="regular")  # ✅ ポイント種別
    balance_after = Column(Integer, nullable=False)  # ✅ 取引後の残高
    created_at = Column(DateTime, server_default=func.now())  # ✅ 取引日時

    # ✅ ユーザーとのリレーション（オプション）
    user = relationship("User", back_populates="point_transactions")

    # ✅ 高速検索用インデックス
    __table_args__ = (
        Index("idx_user_id", "user_id"),  # ✅ ユーザーごとの検索用
        Index("idx_related_id", "related_table", "related_id")  # ✅ 関連取引検索用
    )
