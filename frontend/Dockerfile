# frontend/Dockerfile
FROM node:20-alpine

# 作業ディレクトリ
WORKDIR /app

# 依存インストール
COPY package.json package-lock.json* ./
RUN npm install

# アプリ本体
COPY . .

# Next.js dev サーバ（開発用）
CMD ["npm", "run", "dev"]

# ポート 3000 を明示（任意）
EXPOSE 3000
