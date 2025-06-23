# app/init_data.py
import os
from dotenv import load_dotenv, find_dotenv

# Allow switching environment via ENV_FILE (defaults to production)
ENV_FILE = os.getenv("ENV_FILE", ".env.production")
load_dotenv(find_dotenv(ENV_FILE), override=False)

from .db import Base, SessionLocal, engine, DATABASE_URL, CONNECT_ARGS
from .models import Product
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import quoted_name


# 初回：DBが存在しない場合は作成（MySQL限定）
def create_database_if_not_exists():
    # Use the final DATABASE_URL resolved in app.db
    url = make_url(DATABASE_URL)
    db_name = url.database
    if not db_name:
        raise RuntimeError("DATABASE_URL に DB 名が含まれていません")
    db_name = db_name.partition("?")[0]
    base_url = url.set(database="", query=None)

    quoted_db = quoted_name(db_name, quote=True)

    # DBなし接続エンジンで CREATE DATABASE 実行
    engine_wo_db = create_engine(str(base_url), connect_args=CONNECT_ARGS)
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
