# Python 3.9の公式イメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをプロジェクト全体からコピー
COPY ./app /app/app
COPY requirements.txt /app/requirements.txt

# 必要な依存関係をインストール
RUN pip install --no-cache-dir -r /app/requirements.txt

# デバッグ用: コピーされたファイルを確認
RUN ls /app && ls /app/app && echo $PATH && which uvicorn

# FastAPIアプリを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
