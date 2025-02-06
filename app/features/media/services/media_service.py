import boto3
import os
from dotenv import load_dotenv
from app.features.media.repositories.media_repository import save_media_info, delete_media_info
from sqlalchemy.orm import Session  # ✅ DBセッションのインポート


# ✅ 環境変数の読み込み
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

# ✅ S3クライアントの初期化
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION  # ✅ ここが重要！
)
print(f"[DEBUG] AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}")
print(f"[DEBUG] AWS_S3_BUCKET_NAME: {AWS_S3_BUCKET_NAME}")
print(f"[DEBUG] AWS_S3_REGION: {AWS_S3_REGION}")


# ✅ S3署名付きURLの発行
def generate_presigned_url(file_name: str, file_type: str, target_type: str, target_id: int):
    key = f"{target_type}/{target_id}/{file_name}"
    return s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': AWS_S3_BUCKET_NAME,
            'Key': key,
            'ContentType': file_type
        },
        ExpiresIn=3600  # ✅ 1時間の有効期限
    )

# ✅ アップロード情報をDBに保存
def save_uploaded_file_info(file_url: str, file_type: str, target_type: str, target_id: int, order_index: int):
    save_media_info(file_url, file_type, target_type, target_id, order_index)

# ✅ S3ファイルとDBレコードの削除
from urllib.parse import urlparse

def delete_media_file(media_id: int, db: Session):
    # ✅ DB削除前にメディア情報を取得
    media = delete_media_info(media_id, db)
    if media:
        # ✅ メディア情報の詳細ログ
        print(f"[DEBUG] 取得したメディア情報: {media.__dict__}")

        # ✅ URLから正しいファイルキーを抽出
        parsed_url = urlparse(media.file_url)
        
        # ✅ バケット名を除いた正しいファイルキーを取得
        if f"{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_REGION}.amazonaws.com" in parsed_url.netloc:
            file_key = parsed_url.path.lstrip('/')
        elif "s3.amazonaws.com" in parsed_url.netloc:
            file_key = parsed_url.path.lstrip('/').replace(f"{AWS_S3_BUCKET_NAME}/", "")
        else:
            raise Exception("URL形式が正しくありません")

        print(f"[DEBUG] 正しい削除対象のファイルキー: {file_key}")

        try:
            # ✅ S3オブジェクトの削除
            response = s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=file_key)
            status_code = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
            print(f"[DEBUG] S3削除レスポンス: {response}")

            if status_code == 204:
                print("[INFO] S3ファイル削除成功")
            else:
                print(f"[ERROR] S3ファイル削除失敗: {response}")
                raise Exception(f"S3ファイル削除失敗: {response}")
        except Exception as e:
            print(f"[ERROR] S3削除エラー: {str(e)}")
            raise Exception(f"S3削除に失敗しました: {str(e)}")
    else:
        print(f"[ERROR] media_id={media_id} に対応するメディア情報が見つかりません。")
