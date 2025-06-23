# POS App (Simple)

This repository contains a minimal point-of-sale demo. It includes:

- **backend**: FastAPI service exposing product and transaction APIs.
- **frontend**: Next.js client for the POS interface.
- **MySQL database**: sample schema and data scripts are provided.

## Running with Docker

1. Install Docker and Docker Compose.
2. From the project directory run:

   ```bash
   docker-compose up --build
   ```

3. Visit `http://localhost:3000` to use the web frontend. The API is available at `http://localhost:8000` and MySQL listens on port `3307`.

Stop the containers with `Ctrl+C` and run `docker-compose down` when finished.

## Backend configuration

The API can connect to the database in two ways. If the `DATABASE_URL` environment
variable is set, its value is used directly as the SQLAlchemy connection string.
Otherwise the backend builds the DSN from `DB_USER`, `DB_PASSWORD`, `DB_HOST`,
`DB_PORT` and `DB_NAME`.

Environment variables are loaded from the file specified by `ENV_FILE`. When the
variable is not set, `.env.production` is used.
For local development use the provided development files and start the services
with:

```bash
ENV_FILE=.env.development docker-compose up --build
```


## SSL certificate

The backend verifies connections to Azure Database for MySQL using the DigiCert root certificate. The file `backend/certs/digicert.pem` is copied to `/etc/ssl/certs/digicert.pem` when the Docker image is built and is required for SSL connections.

