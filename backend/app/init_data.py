# app/init_data.py - Azure MySQL Compatible
import os
import time
import pymysql
from urllib.parse import urlparse

# Load environment configuration
from dotenv import load_dotenv, find_dotenv

# Allow switching environment via ENV_FILE (defaults to production)
ENV_FILE = os.getenv("ENV_FILE", ".env.production")
load_dotenv(find_dotenv(ENV_FILE), override=False)

print("DEBUG DB_USER:", os.getenv("DB_USER"))
print("DEBUG DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DEBUG DATABASE_URL:", os.getenv("DATABASE_URL"))

# Test database connectivity with environment-aware connection
def test_connection():
    # Always use individual environment variables for more reliable password handling
    # This avoids URL parsing issues with special characters in passwords
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "pos_app_db")
    
    print(f"=== Connection Details ===")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Password: {'*' * len(password) if password else '(empty)'}")
    print(f"Database: {database}")
    
    # Check if this is Azure MySQL (requires SSL)
    ssl_config = {}
    if host.endswith('.mysql.database.azure.com'):
        ssl_config = {
            'ssl_ca': '/etc/ssl/certs/digicert.pem',
            'ssl_verify_cert': True,
            'ssl_verify_identity': True
        }
        print(f"=== Connecting to Azure MySQL with SSL ===")
    else:
        print(f"=== Connecting to local MySQL ===")
    
    print(f"SSL Config: {ssl_config}")
    print(f"============================")

    # Test connection with retry logic - first try without database, then with database
    for attempt in range(5):
        try:
            # First try connecting without specifying database
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                **ssl_config
            )
            print(f"✅ Server connection successful on attempt {attempt + 1}")
            conn.close()
            
            # Now try with the specific database
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                database=database,
                **ssl_config
            )
            print(f"✅ Database '{database}' connection successful")
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Connection attempt {attempt + 1} failed: {e}")
            if attempt < 4:  # Don't sleep on the last attempt
                time.sleep(3)
    
    # Try just server connection if database connection fails
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            **ssl_config
        )
        print(f"✅ Server connection successful (without specific database)")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Server connection also failed: {e}")
        return False

# Use direct PyMySQL for all database operations since SQLAlchemy fails with Azure SSL
def create_database_if_not_exists():
    """Create database using direct PyMySQL connection"""
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "pos_app_db")
    
    # SSL config for Azure
    ssl_config = {}
    if host.endswith('.mysql.database.azure.com'):
        ssl_config = {
            'ssl_ca': '/etc/ssl/certs/digicert.pem',
            'ssl_verify_cert': True,
            'ssl_verify_identity': True
        }
    
    try:
        # Connect without database to create it
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            **ssl_config
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        conn.commit()
        conn.close()
        print(f"✓ データベース `{database}` の存在を確認（または作成）しました。")
    except Exception as e:
        print(f"⚠️  Database creation failed (may already exist): {e}")
        print(f"   Proceeding with table creation...")


def create_tables():
    """Create tables using direct PyMySQL connection"""
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "pos_app_db")
    
    # SSL config for Azure
    ssl_config = {}
    if host.endswith('.mysql.database.azure.com'):
        ssl_config = {
            'ssl_ca': '/etc/ssl/certs/digicert.pem',
            'ssl_verify_cert': True,
            'ssl_verify_identity': True
        }
    
    # Connect to the database
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database,
        **ssl_config
    )
    
    try:
        with conn.cursor() as cursor:
            # Create products table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                price INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
            """
            cursor.execute(create_table_sql)
        conn.commit()
        print("✓ テーブル定義を作成しました。")
    finally:
        conn.close()


def insert_initial_products():
    """Insert initial products using direct PyMySQL connection"""
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "pos_app_db")
    
    # SSL config for Azure
    ssl_config = {}
    if host.endswith('.mysql.database.azure.com'):
        ssl_config = {
            'ssl_ca': '/etc/ssl/certs/digicert.pem',
            'ssl_verify_cert': True,
            'ssl_verify_identity': True
        }
    
    # Connect to the database
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database,
        **ssl_config
    )
    
    products = [
        {"code": "4901681328401", "name": "P-B3A12-BK", "price": 2000},
        {"code": "4901681328402", "name": "P-B3A12-BL", "price": 2000},
        {"code": "4901681328403", "name": "P-B3A12-R", "price": 2000},
        {"code": "4901681328416", "name": "P-B3A12-S", "price": 2000},
    ]
    
    try:
        with conn.cursor() as cursor:
            for p in products:
                # Check if product already exists
                cursor.execute("SELECT id FROM products WHERE code = %s", (p["code"],))
                if cursor.fetchone():
                    print(f"▶ 商品 {p['code']} は既に登録済み ― スキップ")
                    continue
                
                # Insert new product
                try:
                    cursor.execute(
                        "INSERT INTO products (code, name, price) VALUES (%s, %s, %s)",
                        (p["code"], p["name"], p["price"])
                    )
                    print(f"✓ 追加: {p['code']} {p['name']}")
                except Exception as e:
                    print(f"✗ 失敗 ({p['code']}): {e}")
        conn.commit()
    finally:
        conn.close()


def main():
    print("🚀 Starting Azure MySQL database initialization...")
    
    # Test connection first
    if not test_connection():
        print("❌ Cannot proceed with database initialization - connection failed")
        exit(1)
    
    print("✅ Database connection test passed")
    
    try:
        create_database_if_not_exists()
        create_tables()
        insert_initial_products()
        print("🎉 Database initialization completed successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()
