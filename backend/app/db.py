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


# ---------- CA ファイル ----------
CA_CERT = "/etc/ssl/certs/digicert.pem"    # Dockerfile で配置したパス

# ---------- DSN 組み立て ----------
BASE_DSN = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ・Azure MySQL Flexible Server なら SSL 必須
#   →   *.mysql.database.azure.com で判定
if DB_HOST.endswith(".mysql.database.azure.com"):
    DATABASE_URL = f"{BASE_DSN}?ssl_ca={CA_CERT}&ssl_verify_cert=true"
    CONNECT_ARGS = {}
else:
    # ローカル開発：SSL 無し
    DATABASE_URL = BASE_DSN
    CONNECT_ARGS = {}

# ────────────────────────────────
# SQLAlchemy
# ────────────────────────────────

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args=CONNECT_ARGS,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()
