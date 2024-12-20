# Python 3.9の公式イメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# プロジェクト全体をコピー
COPY . /app

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# デバッグ用: コピーされたファイルとPATHを確認
RUN ls /app && echo $PATH && which uvicorn

# FastAPIアプリを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
