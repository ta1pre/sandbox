from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# .envファイルを読み込み
load_dotenv()

# 環境変数からDATABASE_URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ データベースエンジンの作成（JSTに設定）
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "init_command": "SET time_zone = 'Asia/Tokyo'"  # ✅ タイムゾーン設定
    }
)

# ORMの基盤クラス
Base = declarative_base()

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースセッションを取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
