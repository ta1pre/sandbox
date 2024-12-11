# Python 3.9の公式イメージを使用
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY ./app /app
COPY requirements.txt /app

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# FastAPIアプリを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
