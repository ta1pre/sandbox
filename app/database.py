from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

# .envファイルの読み込み
load_dotenv()

# DATABASE_URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your environment variables or .env file.")

# データベースエンジンとセッション作成
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースモデルの定義
Base = declarative_base()

# usersテーブルのモデル
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nick_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# データベース接続確認用関数
def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return result.fetchone()[0] == 1
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return False
