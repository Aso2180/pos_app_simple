# frontend/Dockerfile - Azure Container Apps Production
#####################  1) Build Stage  #####################
ARG ENV_FILE=.env.production
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm ci --only=production

# Copy environment file
ARG ENV_FILE
COPY ${ENV_FILE} ./.env

# Copy source and build
COPY . .

# Ensure public directory exists (required for COPY in runtime stage)
RUN mkdir -p ./public

RUN npm run build

#####################  2) Runtime Stage ####################
FROM node:20-alpine AS runtime
WORKDIR /app

# Production environment
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy public directory (create empty one in builder if it doesn't exist)
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Switch to non-root user
USER nextjs

# Health check for Container Apps
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

EXPOSE 3000
CMD ["node", "server.js"]
