# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

# .envファイルの読み込み
load_dotenv()

# DATABASE_URLを環境変数から取得
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your environment variables or .env file.")

# データベースエンジンを作成（接続プールを含む設定）
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # プール内の基本接続数
    max_overflow=20,        # 最大接続数
    pool_timeout=30,        # プールの待機タイムアウト（秒）
    pool_recycle=1800,      # アイドル接続再利用のタイムアウト
    pool_pre_ping=True      # 接続確認用のPingを有効化
)

# セッションローカルを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースモデル
Base = declarative_base()

# データベース依存性注入用関数
def get_db():
    """
    データベースセッションを取得するための依存性注入関数
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
