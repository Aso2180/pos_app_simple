# backend/app/models.py
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import (
    Column,
    Integer,
    String,
    CHAR,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db import Base

# ────────────────────────────────
# 商品マスタ (PRD_MST)
# ────────────────────────────────
class Product(Base):
    __tablename__ = "prd_mst"

    prd_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(CHAR(13), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, comment="税抜円")

    # 関連
    details: Mapped[List["TransactionDetail"]] = relationship(
        back_populates="product"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Product {self.code} {self.name} ¥{self.price}>"


# ────────────────────────────────
# 取引ヘッダ (TRD)
# ────────────────────────────────
class Transaction(Base):
    __tablename__ = "trd"

    trd_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    datetime: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    emp_cd: Mapped[str] = mapped_column(CHAR(10), nullable=False)
    store_cd: Mapped[str] = mapped_column(CHAR(5), nullable=False)
    pos_no: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    total_amt: Mapped[int] = mapped_column(Integer, nullable=False)      # 税込
    total_amt_ex: Mapped[int] = mapped_column(Integer, nullable=False)   # 税抜

    details: Mapped[List["TransactionDetail"]] = relationship(
        back_populates="transaction", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Transaction {self.trd_id} ¥{self.total_amt}>"


# ────────────────────────────────
# 取引明細 (TRD_DTL)
# ────────────────────────────────
class TransactionDetail(Base):
    __tablename__ = "trd_dtl"

    trd_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trd.trd_id", ondelete="CASCADE"), primary_key=True
    )
    dtl_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prd_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("prd_mst.prd_id"), nullable=False
    )
    prd_code: Mapped[str] = mapped_column(CHAR(13), nullable=False)
    prd_name: Mapped[str] = mapped_column(String(50), nullable=False)
    prd_price: Mapped[int] = mapped_column(Integer, nullable=False)  # 税抜円
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    line_amount: Mapped[int] = mapped_column(Integer, nullable=False)  # 税抜円
    tax_div: Mapped[str] = mapped_column(CHAR(2), nullable=False, default="10")

    transaction: Mapped["Transaction"] = relationship(back_populates="details")
    product: Mapped["Product"] = relationship(back_populates="details")

    __table_args__ = (UniqueConstraint("trd_id", "dtl_id", name="trd_dtl_pkc"),)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Dtl T{self.trd_id}-{self.dtl_id} {self.prd_code}x{self.quantity}>"
