# app/api/v1/routers/master_router.py

from fastapi import APIRouter

# マスタールーターのインスタンス生成
master_router = APIRouter()

# ✅ LINEBOT関連ルーター
from app.features.linebot.endpoints.linebot_routers import linebot_router
master_router.include_router(linebot_router, prefix="/linebot", tags=["Linebot"])

# ✅ ACCOUNT関連ルーター
from app.features.account.endpoints.account_routers import account_router
master_router.include_router(account_router, prefix="/account", tags=["Account"])

# ✅ SETUP関連ルーター 
from app.features.setup.endpoints.setup_routers import setup_router
master_router.include_router(setup_router, prefix="/setup", tags=["Setup"])

# ✅ SMS関連ルーター
from app.features.sms.endpoints.sms_routers import sms_router
master_router.include_router(sms_router, prefix="/sms", tags=["SMS"])

# ✅ MEDIA関連ルーター
from app.features.media.endpoints.media_routers import media_router
master_router.include_router(media_router, prefix="/media", tags=["Media"])

# ✅ traits関連ルーター
from app.features.cast.traits.endpoints.traits_routers import traits_router
master_router.include_router(traits_router, prefix="/traits", tags=["Traits"])

# ✅ servicetype関連ルーター
from app.features.cast.servicetype.endpoints.servicetype_routers import servicetype_router
master_router.include_router(servicetype_router, prefix="/servicetype", tags=["ServiceType"])

# ✅ ADMIN関連ルーター
from app.features.admin.test_login.endpoints.test_login_routers import test_login_router
master_router.include_router(test_login_router, prefix="/admin/test-login", tags=["Admin"])

# ✅ POINT - ポイント
from app.features.points.endpoints.points_routers import points_routers
master_router.include_router(points_routers, prefix="/points", tags=["Points"])


# ✅ CUSTOMER - 検索API
from app.features.customer.search.endpoints.search_routers import search_router
master_router.include_router(search_router, prefix="/customer/search", tags=["Customer - Search"])

# ✅ CUSTOMER - キャストプロフィール
from app.features.customer.castprof.endpoints.castprof_routers import castprof_router
master_router.include_router(castprof_router, prefix="/customer/castprof", tags=["Customer - CastProf"])

# ✅ CUSTOMER - エリア設定
from app.features.customer.area.endpoints.area_routers import area_router
master_router.include_router(area_router, prefix="/customer/area", tags=["Customer - Area"])

# ✅ RESERVE - 予約
from app.features.reserve.endpoints.reserve_routers import reserve_router
master_router.include_router(reserve_router, prefix="/reserve", tags=["Reserve"])