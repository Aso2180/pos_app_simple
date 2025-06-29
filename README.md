# POS App (Simple) - Azure Container Apps Ready

This repository contains a minimal point-of-sale demo optimized for Azure Container Apps deployment. It includes:

- **backend**: FastAPI service exposing product and transaction APIs
- **frontend**: Next.js client for the POS interface  
- **MySQL database**: Azure MySQL Flexible Server with SSL support

## 🌐 Azure Deployment

### Live Application
- **Frontend**: https://pos-frontend.ashystone-fb341e56.japaneast.azurecontainerapps.io
- **Backend API**: https://pos-backend.ashystone-fb341e56.japaneast.azurecontainerapps.io
- **Database**: posmysqlserver-sea.mysql.database.azure.com:3306

### Azure Architecture
- **Platform**: Azure Container Apps (Japan East)
- **Database**: Azure MySQL Flexible Server with SSL
- **Security**: HTTPS endpoints, CORS protection, SSL database connections

## 🐳 Local Development with Docker

1. Install Docker and Docker Compose
2. From the project directory run:

   ```bash
   docker-compose up --build
   ```

3. Visit `http://localhost:3000` to use the web frontend
4. API available at `http://localhost:8000`
5. MySQL available on port `3306`

Stop with `Ctrl+C` and cleanup with `docker-compose down`

## ⚙️ Configuration

### Environment Files
- `.env.production` - Azure Container Apps configuration
- `.env.development` - Local development configuration

### Database Connection
The API supports two connection methods:

1. **Direct URL** (recommended for Azure):
   ```env
   DATABASE_URL=mysql+pymysql://user:pass@host:port/db?ssl_ca=/etc/ssl/certs/digicert.pem&ssl_verify_cert=true
   ```

2. **Individual variables** (fallback):
   ```env
   DB_HOST=posmysqlserver-sea.mysql.database.azure.com
   DB_USER=adminuser
   DB_PASSWORD=limit500?
   DB_PORT=3306
   DB_NAME=pos_app_db
   ```

### Environment Selection
Environment files are selected via the `ENV_FILE` variable:
- Production: `ENV_FILE=.env.production`
- Development: `ENV_FILE=.env.development` (default for docker-compose)

## 🔒 Security Features

### SSL/TLS Configuration
- **Azure MySQL**: SSL required with DigiCert certificate
- **Certificate Location**: `/etc/ssl/certs/digicert.pem` (installed in Docker images)
- **HTTPS**: All Azure endpoints use HTTPS
- **CORS**: Strict origin validation for cross-domain requests

### Docker Security
- Non-root users in containers
- Health checks for all services
- Production builds with minimal attack surface

## 📋 API Endpoints

- `GET /health` - Health check for Azure Container Apps
- `GET /products/{code}` - Product lookup
- `POST /purchase` - Create transaction
- `GET /transactions/{id}` - Get transaction details
- `POST /init` - Initialize sample data

## 🚀 Deployment Commands

### Azure Container Apps
```bash
# Build and deploy backend
az containerapp up --name pos-backend --source ./backend

# Build and deploy frontend  
az containerapp up --name pos-frontend --source ./frontend
```

### Local Testing
```bash
# Development mode
docker-compose up --build

# Production simulation
ENV_FILE=.env.production docker-compose up --build
```

