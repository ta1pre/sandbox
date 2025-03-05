import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# 📌 プロジェクトのルートパスを `sys.path` に追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📌 `.env` をロード
load_dotenv()

# 📌 FastAPI の `config.py` から `DATABASE_URL` を取得
from app.core.config import DATABASE_URL
from app.db.session import Base  # 📌 SQLAlchemy の `Base` を取得

# 🚨 `DATABASE_URL` が None の場合はエラー
if not DATABASE_URL:
    raise ValueError("🚨 DATABASE_URL が設定されていません！ `.env` を確認してください。")

# 📌 Alembic の設定を取得
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 📌 ログ設定
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 📌 既存の `Base` をターゲットメタデータとして指定
target_metadata = Base.metadata

# 📌 追加: Alembic に「既存のテーブルを削除させない」設定
def include_object(obj, name, type_, reflected, compare_to):
    """
    - `type_ == "table"` の場合、既存のテーブルは削除しないようにする。
    - 既存のテーブルが `compare_to` に `None` でなく存在している場合、削除しない。
    """
    if type_ == "table" and reflected and compare_to is None:
        return False  # ✅ 既存のテーブルは削除させない
    return True  # ✅ それ以外は通常どおり処理

def run_migrations_offline() -> None:
    """オフラインモードでマイグレーションを実行"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        include_object=include_object  # ✅ 削除を防ぐ設定
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """オンラインモードでマイグレーションを実行"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object  # ✅ 削除を防ぐ設定
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
