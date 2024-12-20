from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, test_db_connection, User

app = FastAPI()

# データベースセッションを取得する依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# データベース接続テストエンドポイント
@app.get("/")
def home():
    return {"message": "githubからプッシュ16:46"}

@app.get("/")
def home():
    return {"message": "テスト"}

@app.get("/test-db")
def test_database():
    if test_db_connection():
        return {"message": "Database connection successful"}
    else:
        return {"message": "Database connection failed"}

# usersテーブルのデータを取得するエンドポイント
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    """usersテーブルから全データを取得する"""
    users = db.query(User).all()
    return {"users": users}
