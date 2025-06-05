# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1) 依存インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) アプリ本体
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
