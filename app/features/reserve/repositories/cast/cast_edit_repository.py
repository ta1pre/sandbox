from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.db.models.resv_reservation import ResvReservation
from app.db.models.resv_status_history import ResvStatusHistory
from app.db.models.resv_reservation_option import ResvReservationOption
from app.features.reserve.schemas.cast.cast_edit_schema import CustomOption


from app.db.models.station import Station

def update_reservation(
    db: Session,
    reservation_id: int,
    start_time: datetime,
    end_time: datetime,
    location: str,
    reservation_note: Optional[str],
    status: str
) -> ResvReservation:
    """予約本体の情報を更新する"""
    
    # 予約レコードを取得
    reservation = db.query(ResvReservation).filter(
        ResvReservation.id == reservation_id
    ).first()
    
    if not reservation:
        return None
    
    # 予約情報を更新
    reservation.start_time = start_time
    reservation.end_time = end_time
    reservation.status = status
    reservation.reservation_note = reservation_note
    
    # locationの処理
    # 1. 数値のみ（駅ID）の場合
    if location and location.strip().isdigit():
        # 駅IDとして取り扱い
        reservation.location = location.strip()
        # 駅に関連する緯度経度を設定
        try:
            station = db.query(Station).filter(Station.id == int(location.strip())).first()
            if station and station.lat and station.lon:
                reservation.latitude = station.lat
                reservation.longitude = station.lon
        except Exception as e:
            print(f"DEBUG - 駅情報取得エラー: {e}")
    # 2. 「緯度,経度」フォーマットの場合
    else:
        reservation.location = location
        try:
            parts = location.split(',')
            if len(parts) == 2:
                latitude, longitude = parts
                reservation.latitude = float(latitude.strip())
                reservation.longitude = float(longitude.strip())
        except (ValueError, AttributeError) as e:
            print(f"DEBUG - 位置情報解析エラー: {e}")
            # フォーマットが不正な場合は位置情報更新をスキップ
            pass
    
    db.commit()
    db.refresh(reservation)
    return reservation


def add_status_history(
    db: Session,
    reservation_id: int,
    prev_status: str,
    new_status: str = "waiting_user_confirm",
    changed_by: str = "cast"
) -> ResvStatusHistory:
    """ステータス履歴を追加する"""
    
    status_history = ResvStatusHistory(
        reservation_id=reservation_id,
        changed_by=changed_by,
        prev_status=prev_status,
        new_status=new_status,
        status_time=datetime.now()
    )
    
    db.add(status_history)
    db.commit()
    db.refresh(status_history)
    return status_history


from app.db.models.point_details import PointDetailsOption

def update_reservation_options(
    db: Session,
    reservation_id: int,
    option_ids: List[int],
    custom_options: List[CustomOption]
) -> bool:
    """予約オプションを全て入れ替える"""
    
    print(f"DEBUG - [リポジトリ層] オプション更新開始: 予約ID={reservation_id}")
    print(f"DEBUG - [リポジトリ層] 選択オプション: {option_ids}")
    print(f"DEBUG - [リポジトリ層] カスタムオプション数: {len(custom_options)}個")
    
    try:
        # リクエスト内容をDBログに残す（デバッグ用）
        print(f"DEBUG - [リポジトリ層] カスタムオプション内容:")
        for i, opt in enumerate(custom_options):
            print(f"  #{i+1}: name={opt.name}, price={opt.price}")
    
        # 既存のオプションを全て論理削除 (ソフトデリート)
        db.query(ResvReservationOption).filter(
            ResvReservationOption.reservation_id == reservation_id
        ).update({"status": "removed"}, synchronize_session=False)
        
        print(f"DEBUG - [リポジトリ層] 既存オプションを論理削除済み")
        
        # 現在のDB状態を確認
        current_options = db.query(ResvReservationOption).filter(
            ResvReservationOption.reservation_id == reservation_id
        ).all()
        print(f"DEBUG - [リポジトリ層] 現在のオプション数: {len(current_options)}")
        for opt in current_options:
            print(f"  ID={opt.option_id}, custom_name={opt.custom_name}, status={opt.status}")
        
        # マスターオプションを登録
        for option_id in option_ids:
            # マスターからオプション情報を取得
            master_option = db.query(PointDetailsOption).filter(
                PointDetailsOption.id == option_id
            ).first()
            
            option_price = 0
            if master_option:
                option_price = master_option.price
                print(f"DEBUG - [リポジトリ層] マスターオプション取得: ID={option_id}, 価格={option_price}")
            else:
                print(f"DEBUG - [リポジトリ層] マスターオプション未取得: ID={option_id}")
                
            # 既存のオプションを確認し、存在する場合は再アクティベート
            existing_option = db.query(ResvReservationOption).filter(
                ResvReservationOption.reservation_id == reservation_id,
                ResvReservationOption.option_id == option_id
            ).first()
            
            if existing_option:
                print(f"DEBUG - [リポジトリ層] 既存オプション再アクティベート: ID={option_id}")
                existing_option.option_price = option_price
                existing_option.status = "active"
                existing_option.custom_name = None
            else:
                # 新規オプションの場合
                print(f"DEBUG - [リポジトリ層] 新規オプション追加: ID={option_id}, 価格={option_price}")
                option = ResvReservationOption(
                    reservation_id=reservation_id,
                    option_id=option_id,
                    option_price=option_price,
                    custom_name=None,
                    status="active"
                )
                db.add(option)
        
        # カスタムオプションを登録する前にまず既存のカスタムオプションをすべて物理削除
        # これにより重複を完全に防止
        db.query(ResvReservationOption).filter(
            ResvReservationOption.reservation_id == reservation_id,
            ResvReservationOption.option_id == 0  # カスタムオプションはoption_id=0
        ).delete(synchronize_session=False)
        
        print(f"DEBUG - [リポジトリ層] 既存のカスタムオプションを削除済み")
        
        # カスタムオプションを登録（一意の名前をチェックして重複防止）
        custom_option_names = set()  # 登録済み名前を追跡
        
        for i, custom in enumerate(custom_options):
            # 同じ名前のカスタムオプションがすでに処理されていれば、重複としてスキップ
            if custom.name in custom_option_names:
                print(f"DEBUG - [リポジトリ層] カスタムオプション重複スキップ: 名前={custom.name}")
                continue
                
            # 名前を追跡リストに追加
            custom_option_names.add(custom.name)
            
            print(f"DEBUG - [リポジトリ層] カスタムオプション追加 #{i+1}: 名前={custom.name}, 価格={custom.price}")
            option = ResvReservationOption(
                reservation_id=reservation_id,
                option_id=0,  # カスタムオプションの場合は0を設定
                option_price=custom.price,
                custom_name=custom.name,
                status="active"
            )
            db.add(option)
        
        # 最終的な状態を確認
        all_options = db.query(ResvReservationOption).filter(
            ResvReservationOption.reservation_id == reservation_id
        ).all()
        
        print(f"DEBUG - [リポジトリ層] オプション更新後の総数: {len(all_options)}個")
        print(f"DEBUG - [リポジトリ層] アクティブなオプション数: {len([o for o in all_options if o.status == 'active'])}個")
        print(f"DEBUG - [リポジトリ層] カスタムオプション数: {len([o for o in all_options if o.status == 'active' and o.option_id == 0])}個")
        
        # コミット
        db.commit()
        print(f"DEBUG - [リポジトリ層] オプション更新完了: コミット成功")
        return True
    except Exception as e:
        print(f"ERROR - [リポジトリ層] オプション更新中にエラー発生: {str(e)}")
        db.rollback()
        return False


def verify_reservation_ownership(
    db: Session, 
    reservation_id: int, 
    cast_id: int
) -> bool:
    """予約オーナーシップ確認（他人の予約を編集できないようにする）"""
    
    reservation = db.query(ResvReservation).filter(
        ResvReservation.id == reservation_id,
        ResvReservation.cast_id == cast_id
    ).first()
    
    return reservation is not None
