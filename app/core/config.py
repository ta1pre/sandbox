import os
from dotenv import load_dotenv

# 環境変数を読み込む
# ✅ `.env` のパスを明示的に指定
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))  # 適切なパスを指定
load_dotenv(dotenv_path, override=True)

print("=== ENVIRONMENT VARIABLES ===")
for key, value in os.environ.items():
    if "REDIRECT" in key.upper():  # `REDIRECT_URI` に関係する変数だけ表示
        print(f"{key} = {value}")
print("=== END ENV ===")

# LINE API関連
LINE_LOGIN_CHANNEL_ID = os.getenv("LINE_LOGIN_CHANNEL_ID")
LINE_LOGIN_CHANNEL_SECRET = os.getenv("LINE_LOGIN_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# ✅ `TEST_VARIABLE` を読み込む
TEST_VARIABLE = os.getenv("TEST_VARIABLE")
print(f"DEBUG: TEST_VARIABLE = {TEST_VARIABLE}")
print(f"DEBUG: REDIRECT_URI = {REDIRECT_URI}")  # ここで値を確認


# フロントエンドURL
FRONTEND_URL = os.getenv("FRONTEND_URL")

# JWT関連
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your_refresh_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS",60))
# OpenAI API関連
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# microCMS
MICROCMS_API_URL= os.getenv("MICROCMS_API_URL")
MICROCMS_API_KEY= os.getenv("MICROCMS_API_KEY")

