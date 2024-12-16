# ファイル名: app/main.py

from fastapi import FastAPI

app = FastAPI()

# 環境変数を使ったエンドポイント
@app.get("/")
def read_root():
    return {"message": "こんにちわ"}  # 環境変数の影響を受けない固定文字列

# 新しいエンドポイント
@app.get("/test")
def test_endpoint():
    return {"message": "This is a test endpoint!"}
