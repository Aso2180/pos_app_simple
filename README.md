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
