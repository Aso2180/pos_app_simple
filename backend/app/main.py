# backend/app/main.py
from __future__ import annotations
from dotenv import load_dotenv, find_dotenv
import os

ENV_FILE = os.getenv("ENV_FILE", ".env.production")
load_dotenv(find_dotenv(ENV_FILE), override=False)
from datetime import datetime
from typing import List, Optional
from decimal import Decimal, ROUND_HALF_UP

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, PositiveInt, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import Product, Transaction, TransactionDetail

from app.init_data import main as init_main

# ✅ FastAPI instance with enhanced configuration for Azure
app = FastAPI(
    title="POS API MVP", 
    version="0.1.0",
    description="Point of Sale API for Azure Container Apps",
    docs_url="/docs" if os.getenv("ENV") != "production" else None,  # Disable docs in production
    redoc_url="/redoc" if os.getenv("ENV") != "production" else None,
)

# Health check endpoint for Azure Container Apps
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "pos-backend"}

# ✅ 初期化エンドポイント（あとで削除OK）
@app.post("/init")
def initialize_data():
    init_main()
    return {"message": "初期データ登録完了"}

# ★──── Enhanced CORS Configuration for Azure ────★
# Parse FRONTEND_ORIGIN environment variable (supports comma-separated list)
frontend_origins = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in frontend_origins.split(",") if origin.strip()]

# Add additional Azure-specific origins
azure_origins = [
    "https://pos-frontend.ashystone-fb341e56.japaneast.azurecontainerapps.io",
    "https://pos-backend.ashystone-fb341e56.japaneast.azurecontainerapps.io"  # For API docs
]

# Combine all origins and remove duplicates
all_origins = list(set(allowed_origins + azure_origins))

# Configure CORS middleware with enhanced security
app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_origin_regex=None,  # Strict origin checking
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specific methods only
    allow_headers=[
        "Accept",
        "Accept-Language", 
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
    ],
    expose_headers=["X-Total-Count"],  # For pagination
    max_age=3600,  # Cache preflight requests for 1 hour
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
TAX_RATE = Decimal("0.10")  # 10% 固定

class ProductOut(BaseModel):
    prd_id: int = Field(..., alias="id")
    code: str
    name: str
    price_ex_tax: int
    price_in_tax: int
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class PurchaseItemIn(BaseModel):
    prd_id: int
    quantity: PositiveInt

class PurchaseRequest(BaseModel):
    emp_cd: Optional[str] = ""
    store_cd: Optional[str] = ""
    pos_no: Optional[str] = ""
    items: List[PurchaseItemIn]

class PurchaseResponse(BaseModel):
    success: bool
    transaction_id: int
    total_amount: int
    total_amount_ex: int

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
    product = (
        db.query(Product)
        .filter((Product.code == code) | (func.right(Product.code, 6) == code))
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
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
    if not payload.items:
        raise HTTPException(status_code=400, detail="items list is empty")

    emp_cd = payload.emp_cd or "9999999999"
    store_cd = payload.store_cd or "30"
    pos_no = payload.pos_no or "90"

    total_ex = 0
    for item in payload.items:
        product: Product | None = db.query(Product).filter(Product.prd_id == item.prd_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product id {item.prd_id} not found")
        total_ex += product.price * item.quantity

    total_in = int(Decimal(total_ex * (1 + TAX_RATE)).quantize(0, ROUND_HALF_UP))

    transaction = Transaction(
        datetime=datetime.utcnow(),
        emp_cd=emp_cd,
        store_cd=store_cd,
        pos_no=pos_no,
        total_amt=total_in,
        total_amt_ex=total_ex,
    )
    db.add(transaction)
    db.flush()

    seq = 1
    for item in payload.items:
        product = db.query(Product).filter(Product.prd_id == item.prd_id).first()
        assert product is not None
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

# ---------------------------------------------------------------------------
# 3) 取引参照
# ---------------------------------------------------------------------------
@app.get("/transactions/{trd_id}", response_model=TransactionOut)
def read_transaction(trd_id: int, db: Session = Depends(get_db)):
    trd = db.query(Transaction).filter(Transaction.trd_id == trd_id).first()
    if not trd:
        raise HTTPException(status_code=404, detail="transaction not found")

    dtls = db.query(TransactionDetail).filter(TransactionDetail.trd_id == trd_id).all()

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
