# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1) Microsoft が公開しているルート CA を追加
ADD https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem /usr/local/share/ca-certificates/baltimore.pem
RUN update-ca-certificates

# 2) 依存インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) アプリ本体
COPY app ./app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# backend/Dockerfile 末尾を変更
CMD ["sh", "-c", "python -m app.init_data || true && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
