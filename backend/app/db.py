# backend/app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ────────────────────────────────
# 環境変数（.env）を利用
# ────────────────────────────────
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "limit500?")
DB_HOST = os.getenv("DB_HOST", "pos-db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "pos_app_db")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ────────────────────────────────
# SQLAlchemy
# ────────────────────────────────
SSL_CA_PATH = "/etc/ssl/certs/baltimore.pem"      # もしくは /usr/local/share/ca-certificates/baltimore.pem

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={
        "ssl": {"ca": SSL_CA_PATH}
    }
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()
