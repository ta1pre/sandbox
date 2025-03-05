from fastapi import FastAPI
from app.api.v1.routers.master_router import master_router  # 直接指定
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(
    level=logging.INFO,  # ✅ INFO レベルのログを出力
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # ✅ ターミナルに出力
    ]
)

logger = logging.getLogger(__name__)


app = FastAPI()

# API全体のルーターを1行で登録
app.include_router(master_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"msg": "Hello from main!"}

origins = [
    "https://8c0b37dc5a6a.ngrok.app",  # フロントエンドのドメインを指定
    "http://localhost:3000",  # ローカル開発用
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # `*` ではなく、特定のドメインを指定
    allow_credentials=True,  # `withCredentials: true` を許可
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)