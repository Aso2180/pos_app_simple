# app/init_data.py (冒頭に追加)
from app.db import Base, engine
import app.models
Base.metadata.create_all(bind=engine)

# backend/app/init_data.py
from sqlalchemy.exc import IntegrityError

from .db import SessionLocal
from .models import Product

INIT_PRODUCTS = [
    {"code": "4901681328401", "name": "P-B3A12-BK", "price": 2000},
    {"code": "4901681328402", "name": "P-B3A12-BL", "price": 2000},
    {"code": "4901681328403", "name": "P-B3A12-R",  "price": 2000},
    {"code": "4901681328416", "name": "P-B3A12-S",  "price": 2000},
]

def main() -> None:
    db = SessionLocal()
    for p in INIT_PRODUCTS:
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

if __name__ == "__main__":
    main()
