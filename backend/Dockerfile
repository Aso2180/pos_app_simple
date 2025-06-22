# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# CA証明書の追加
COPY ./certs/digicert.pem /usr/local/share/ca-certificates/digicert.crt
RUN chmod 644 /usr/local/share/ca-certificates/digicert.crt \
    && update-ca-certificates

# 2) 依存インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) アプリ本体
COPY app ./app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# backend/Dockerfile 末尾を変更
CMD ["sh", "-c", "python -m app.init_data || true && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
