from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    # 環境変数から設定を読み込む
    message = os.getenv("MESSAGE", "Hello, World!")
    return {"message": message}
