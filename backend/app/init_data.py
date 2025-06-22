# app/init_data.py
import os

from app.db import CA_CERT, Base, SessionLocal, engine
from app.models import Product
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import quoted_name

load_dotenv(dotenv_path=".env.production")


# 初回：DBが存在しない場合は作成（MySQL限定）
def create_database_if_not_exists():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL 環境変数が未設定です")

    # parse DATABASE_URL and remove database/query components
    url = make_url(db_url)
    db_name = url.database
    if db_name:
        db_name = db_name.partition("?")[0]
    base_url = url.set(database="", query=None)

    quoted_db = quoted_name(db_name, quote=True)

    # DBなし接続エンジンで CREATE DATABASE 実行
    engine_wo_db = create_engine(str(base_url), connect_args={"ssl": {"ca": CA_CERT}})
    with engine_wo_db.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS {quoted_db} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            )
        )
        print(f"✓ データベース `{db_name}` の存在を確認（または作成）しました。")


# 初回：テーブル作成
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✓ テーブル定義を作成しました。")


# 初回：商品データの登録
def insert_initial_products():
    db = SessionLocal()
    for p in [
        {"code": "4901681328401", "name": "P-B3A12-BK", "price": 2000},
        {"code": "4901681328402", "name": "P-B3A12-BL", "price": 2000},
        {"code": "4901681328403", "name": "P-B3A12-R", "price": 2000},
        {"code": "4901681328416", "name": "P-B3A12-S", "price": 2000},
    ]:
        exists = db.query(Product).filter(Product.code == p["code"]).first()
        if exists:
            print(f"▶ 商品 {p['code']} は既に登録済み ― スキップ")
            continue
        try:
            db.add(Product(**p))
            db.commit()
            print(f"✓ 追加: {p['code']} {p['name']}")
        except IntegrityError as e:
            db.rollback()
            print(f"✗ 失敗 ({p['code']}):", e.orig)
    db.close()


def main():
    create_database_if_not_exists()
    create_tables()
    insert_initial_products()


if __name__ == "__main__":
    main()
