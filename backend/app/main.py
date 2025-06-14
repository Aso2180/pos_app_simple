# backend/app/main.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from decimal import Decimal, ROUND_HALF_UP

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware    # ← 追加
from pydantic import BaseModel, PositiveInt, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import Product, Transaction, TransactionDetail

import os
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

TAX_RATE = Decimal("0.10")  # 10% 固定

app = FastAPI(title="POS API MVP", version="0.1.0")

# ★──── CORS middleware ────★
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ★──────────────────────★

# ---------------------------------------------------------------------------
# DB セッション依存
# ---------------------------------------------------------------------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Pydantic スキーマ
# ---------------------------------------------------------------------------


class ProductOut(BaseModel):
    """商品検索レスポンス"""

    prd_id: int = Field(..., alias="id")
    code: str
    name: str
    price_ex_tax: int  # 税抜円
    price_in_tax: int  # 税込円

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PurchaseItemIn(BaseModel):
    """購入リクエスト：商品 1 行"""

    prd_id: int
    quantity: PositiveInt


class PurchaseRequest(BaseModel):
    """購入リクエスト：全明細"""

    emp_cd: Optional[str] = ""  # 空の場合デフォルト値
    store_cd: Optional[str] = ""  # 空→'30'
    pos_no: Optional[str] = ""  # 空→'90'
    items: List[PurchaseItemIn]


class PurchaseResponse(BaseModel):
    """購入レスポンス"""

    success: bool
    transaction_id: int
    total_amount: int  # 税込
    total_amount_ex: int  # 税抜

# ─── 取引参照用スキーマ ────────────────────
class TransactionLine(BaseModel):
    prd_name: str
    quantity: int
    price_in_tax: int
    line_amount: int

class TransactionOut(BaseModel):
    transaction_id: int
    total_amount_ex: int
    total_amount: int
    items: List[TransactionLine]


# ---------------------------------------------------------------------------
# 1) 商品マスタ検索
# ---------------------------------------------------------------------------


@app.get("/products/{code}", response_model=ProductOut)
def read_product(code: str, db: Session = Depends(get_db)):
    """
    商品コード（JAN13 でも 6 桁でも可）で 1 件検索
    """
    product = (
        db.query(Product)
        .filter((Product.code == code) | (func.right(Product.code, 6) == code))
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    
    # A) assert で確定させる
    assert product is not None

    return {
        "id": product.prd_id,
        "code": product.code,
        "name": product.name,
        "price_ex_tax": product.price,
        "price_in_tax": int(Decimal(product.price) * (1 + TAX_RATE)),
    }


# ---------------------------------------------------------------------------
# 2) 購入登録
# ---------------------------------------------------------------------------


@app.post("/purchase", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(payload: PurchaseRequest, db: Session = Depends(get_db)):
    """
    - 取引ヘッダ & 明細を登録  
    - 合計金額（税抜/税込）を算出して返却
    """
    if not payload.items:
        raise HTTPException(status_code=400, detail="items list is empty")

    # ---------- デフォルト値補完 ----------
    emp_cd = payload.emp_cd or "9999999999"
    store_cd = payload.store_cd or "30"
    pos_no = payload.pos_no or "90"

    # ---------- 商品存在チェック & 金額集計 ----------
    total_ex = 0
    for item in payload.items:
        product: Product | None = db.query(Product).filter(Product.prd_id == item.prd_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product id {item.prd_id} not found",
            )
        assert product is not None  # ← 追加
        total_ex += product.price * item.quantity

    total_in = int(Decimal(total_ex * (1 + TAX_RATE)).quantize(0, ROUND_HALF_UP))

    # ---------- 取引ヘッダ INSERT ----------
    transaction = Transaction(
        datetime=datetime.utcnow(),
        emp_cd=emp_cd,
        store_cd=store_cd,
        pos_no=pos_no,
        total_amt=total_in,
        total_amt_ex=total_ex,
    )
    db.add(transaction)
    db.flush()  # 自動採番した TRD_ID を得る

    # ---------- 取引明細 INSERT ----------
    seq = 1
    for item in payload.items:
        product = db.query(Product).filter(Product.prd_id == item.prd_id).first()

        assert product is not None  # ★ ここを追加
        
        detail = TransactionDetail(
            trd_id=transaction.trd_id,
            dtl_id=seq,
            prd_id=product.prd_id,
            prd_code=product.code,
            prd_name=product.name,
            prd_price=product.price,
            quantity=item.quantity,
            line_amount=product.price * item.quantity,
        )
        db.add(detail)
        seq += 1

    db.commit()
    db.refresh(transaction)

    return PurchaseResponse(
        success=True,
        transaction_id=transaction.trd_id,
        total_amount=transaction.total_amt,
        total_amount_ex=transaction.total_amt_ex,
    )

# ─── 新エンドポイント ─────────────────────
@app.get("/transactions/{trd_id}", response_model=TransactionOut)
def read_transaction(trd_id: int, db: Session = Depends(get_db)):
    trd = db.query(Transaction).filter(Transaction.trd_id == trd_id).first()
    if not trd:
        raise HTTPException(status_code=404, detail="transaction not found")

    dtls = (
        db.query(TransactionDetail)
        .filter(TransactionDetail.trd_id == trd_id)
        .all()
    )

    items = [
        TransactionLine(
            prd_name=d.prd_name,
            quantity=d.quantity,
            price_in_tax=d.prd_price,
            line_amount=d.line_amount,
        )
        for d in dtls
    ]

    return TransactionOut(
        transaction_id=trd.trd_id,
        total_amount_ex=trd.total_amt_ex,
        total_amount=trd.total_amt,
        items=items,
    )

