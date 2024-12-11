from mangum import Mangum

# 既存のFastAPIアプリ
app = FastAPI()

@app.get("/")
def read_root():
    # 環境変数から設定を読み込む
    message = os.getenv("MESSAGE", "Hello, World!")
    return {"message": message}

# Lambdaエントリポイント
handler = Mangum(app)
