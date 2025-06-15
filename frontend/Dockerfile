#####################  1) Build Stage  #####################
# 追加（デフォルトを本番用に）
ARG ENV_FILE=.env.production

FROM node:20-alpine AS builder

WORKDIR /app

# 依存だけ先にコピーするとキャッシュが効く
COPY package*.json ./
# もう一度宣言（実引数を受け取る）
ARG ENV_FILE
# ここで .env を取り込む
COPY ${ENV_FILE} ./.env
RUN npm ci          

# アプリ本体をコピーしてビルド
COPY . .
RUN npm run build  

#####################  2) Runtime Stage ####################
FROM node:20-alpine AS runtime
WORKDIR /app

# 本番モード
ENV NODE_ENV=production
ENV PORT=3000

# builder の成果物だけ取り込む
COPY --from=builder /app .

EXPOSE 3000
CMD ["npm", "start"]
