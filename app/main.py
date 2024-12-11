from fastapi import FastAPI
import os
from mangum import Mangum  # Mangumをインポート

app = FastAPI()

@app.get("/")
def read_root():
    # 環境変数から設定を読み込む
    message = os.getenv("MESSAGE", "Hello, World!")
    return {"message": message}

# Lambdaエントリポイント
handler = Mangum(app)
