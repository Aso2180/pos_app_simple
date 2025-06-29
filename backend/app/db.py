# backend/app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv, find_dotenv

ENV_FILE = os.getenv("ENV_FILE", ".env.production")
load_dotenv(find_dotenv(ENV_FILE), override=False)

# ────────────────────────────────
# 環境変数（.env）を利用
# ────────────────────────────────
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "limit500?") 
DB_HOST = os.getenv("DB_HOST", "pos-db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "pos_app_db")

# ---------- CA ファイル ----------
CA_CERT = "/etc/ssl/certs/digicert.pem"  # Dockerfile で配置したパス

# Allow full connection string via DATABASE_URL
DATABASE_URL_ENV = os.getenv("DATABASE_URL")


if DATABASE_URL_ENV:
    # Use provided connection string directly
    DATABASE_URL = DATABASE_URL_ENV

    # If connecting to Azure MySQL, ensure CA file is explicitly passed
    if "mysql.database.azure.com" in DATABASE_URL_ENV:
        CONNECT_ARGS = {"ssl": {"ca": CA_CERT}}
    else:
        CONNECT_ARGS = {}
else:
    # ---------- DSN 組み立て ----------
    # PASSWORD に記号が含まれていても正しく接続できるよう URL.create() を利用
    BASE_DSN = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
    )

    # ・Azure MySQL Flexible Server なら SSL 必須
    #   →   *.mysql.database.azure.com で判定
    if DB_HOST.endswith(".mysql.database.azure.com"):
        # Use direct parameter mapping that works in PyMySQL test
        DATABASE_URL = str(BASE_DSN)
        CONNECT_ARGS = {
            "ssl_ca": CA_CERT,
            "ssl_verify_cert": True,
            "ssl_verify_identity": True
        }
    else:
        # ローカル開発：SSL 無し
        DATABASE_URL = str(BASE_DSN)
        CONNECT_ARGS = {}

# ────────────────────────────────
# SQLAlchemy
# ────────────────────────────────

print(f"🔧 DATABASE_URL: {DATABASE_URL}")
print(f"🔧 CONNECT_ARGS: {CONNECT_ARGS}")

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
