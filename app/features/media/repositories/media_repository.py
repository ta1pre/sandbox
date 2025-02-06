from sqlalchemy.orm import Session
from app.db.models.media_files import MediaFile

# ✅ メディアファイルの登録
def save_media_info(file_url: str, file_type: str, target_type: str, target_id: int, order_index: int, db: Session):
    media = MediaFile(
        file_url=file_url,
        file_type=file_type,
        target_type=target_type,
        target_id=target_id,
        order_index=order_index
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media

# ✅ メディアファイルとS3の削除
def delete_media_info(media_id: int, db: Session):
    media = db.query(MediaFile).filter(MediaFile.id == media_id).first()
    if media:
        db.delete(media)
        db.commit()
        return media
    return None
