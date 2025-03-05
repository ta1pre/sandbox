from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func, text
from app.db.session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nick_name = Column(String(255), nullable=True)
    prefectures = Column(String(255), nullable=True)
    line_id = Column(String(255), unique=True, nullable=False, index=True)
    invitation_id = Column(String(255), unique=True, nullable=True, index=True)
    tracking_id = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    email_verified = Column(Boolean, default=False)
    mobile_phone = Column(String(255), nullable=True)
    phone_verification_code = Column(String(6), nullable=True)
    phone_verified = Column(Boolean, default=False)
    picture_url = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=True)
    sex = Column(String(255), nullable=True)
    birth = Column(String(255), nullable=True)
    user_type = Column(String(255), nullable=True)
    affi_type = Column(Integer, nullable=True)
    last_login = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime,server_default=func.now(),onupdate=text("CONVERT_TZ(NOW(), 'UTC', 'Asia/Tokyo')") )
    setup_status = Column(String(50), nullable=True, default=None)

    def __repr__(self):
        return f"<User(id={self.id}, line_id={self.line_id}, email={self.email}, setup_status={self.setup_status})>"
