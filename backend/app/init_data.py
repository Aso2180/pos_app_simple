# app/init_data.py
import pymysql
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.production")
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text, create_engine
from app.db import SessionLocal, Base, engine
from app.models import Product
import os

# 初回：DBが存在しない場合は作成（MySQL限定）
def create_database_if_not_exists():
    # DATABASE_URL から DB名を抜いた接続文字列を作成（スキーマ無し）
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL 環境変数が未設定です")

    # 例: mysql+pymysql://user:pass@host:3306/pos_app_db から
    #     mysql+pymysql://user:pass@host:3306 にする
    base_url = db_url.rsplit("/", 1)[0]
    db_name = db_url.rsplit("/", 1)[1].split("?")[0]  # pos_app_db

    # DBなし接続エンジンで CREATE DATABASE 実行
    engine_wo_db = create_engine(base_url)
    with engine_wo_db.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"))
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
        {"code": "4901681328403", "name": "P-B3A12-R",  "price": 2000},
        {"code": "4901681328416", "name": "P-B3A12-S",  "price": 2000},
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
