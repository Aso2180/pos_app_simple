#####################  1) Build Stage  #####################
FROM node:20-alpine AS builder

WORKDIR /app

# 依存だけ先にコピーするとキャッシュが効く
COPY package*.json ./
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
