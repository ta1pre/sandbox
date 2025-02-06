from fastapi import FastAPI
from app.api.v1.routers.master_router import master_router  # 直接指定
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# API全体のルーターを1行で登録
app.include_router(master_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"msg": "Hello from main!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のドメインに絞るべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

