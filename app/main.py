# ファイル名: app/main.py

from fastapi import FastAPI
import json  # jsonモジュールをインポート

app = FastAPI()

@app.get("/")
def read_root():
    return json.dumps({"message": "ギットハブからこんにちわぁ〜〜〜"}, ensure_ascii=False)  # Falseは大文字

# 新しいエンドポイント
@app.get("/test")
def test_endpoint():
    return json.dumps({"message": "ギットハブからこんにちわぁ〜〜〜"}, ensure_ascii=False)  # Falseは大文字
