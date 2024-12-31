# app/main.py

import os
from fastapi import FastAPI
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

app = FastAPI()

# 環境変数の取得
DATABASE_URL = os.getenv("DATABASE_URL", "Not Set")
SECRET_KEY = os.getenv("TEST_KEY", "Not Set")


@app.get("/")
async def root():
    return {
        "message": "1230-1532！",
        "DATABASE_URL": DATABASE_URL,
        "SECRET_KEY": SECRET_KEY
    }


@app.get("/test")
async def test():
    return {"message": "てすとぺーじ"}
