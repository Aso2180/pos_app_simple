# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# CA証明書は追加済み
# COPY ./certs/digicert.pem /usr/local/share/ca-certificates/digicert.pem
# RUN chmod 644 /usr/local/share/ca-certificates/digicert.pem \
    # && update-ca-certificates
COPY ./certs/digicert.pem /etc/ssl/certs/digicert.pem

# 2) 依存インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) アプリ本体
COPY app ./app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# backend/Dockerfile 末尾を変更
CMD ["sh", "-c", "python -m app.init_data || true && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
