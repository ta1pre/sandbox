# app/db/check.py

from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from .session import engine

def test_db_connection():
    """
    データベース接続をテストする関数
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return result.fetchone()[0] == 1
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        return False
