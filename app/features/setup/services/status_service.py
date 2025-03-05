# app/features/setup/services/status_service.py

from sqlalchemy.orm import Session
from app.db.models.cast_common_prof import CastCommonProf
from app.features.media.services.media_delete import delete_s3_file
from app.features.media.repositories.media_repository import delete_media_records
from app.db.models.media_files import MediaFile
from app.db.models.user import User


def delete_cast_profile(user_id: int, db: Session):
    """
    指定した user_id に対応する CastCommonProf を削除する。
    もし存在しない場合でもエラーを発生させずにスルーする。

    Args:
        user_id (int): ユーザーID
        db (Session): SQLAlchemy セッション
    """
    cast_profile = db.query(CastCommonProf).filter(CastCommonProf.cast_id == user_id).first()
    if cast_profile:
        db.delete(cast_profile)
        db.commit()
        
def delete_user_media_files(user_id: int, db: Session):
    """
    指定ユーザーの関連メディアファイルを S3 + DB から削除する。

    Args:
        user_id (int): 削除対象のユーザーID
        db (Session): SQLAlchemy の DB セッション

    Returns:
        bool: 削除処理が成功したかどうか
    """
    # ✅ 1. DB から `target_id == user_id` のメディアを取得
    media_files = db.query(MediaFile).filter(MediaFile.target_id == user_id).all()

    if not media_files:
        print("[INFO] ℹ️ 削除対象のメディアなし")
        return False

    print(f"[INFO] 🗑️ ユーザー {user_id} のメディア {len(media_files)} 件を削除")

    # ✅ 2. S3 から削除
    for media in media_files:
        print(f"[INFO] 🗑️ S3 から削除するファイル: {media.file_url}")
        if not delete_s3_file(media.file_url):
            print(f"[ERROR] ❌ S3 の削除に失敗: {media.file_url}")
            continue  # 失敗しても次の処理を続行

    # ✅ 3. DB から削除
    print("[INFO] 🗑️ DB からメディア削除を開始")
    for media in media_files:
        delete_media_records(db, media.target_type, media.target_id, media.order_index)

    print("[INFO] ✅ 画像削除成功")
    return True

def update_user_setup_status(user_id: int, db: Session):
    """
    ユーザーの `setup_status` を `completed` に更新する。

    Args:
        user_id (int): 更新対象のユーザーID
        db (Session): SQLAlchemy の DB セッション
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.setup_status = "completed"
        db.commit()
        print(f"[INFO] ✅ ユーザー {user_id} の setup_status を 'completed' に更新")