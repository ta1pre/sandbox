# Dockerfile

# Python 3.9の公式イメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なフォルダとファイルを正確にコピー
COPY ./app /app/app
COPY ./requirements.txt /app/

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# デバッグ用: コピーされたファイルを確認
RUN ls /app/app

# FastAPIアプリを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
