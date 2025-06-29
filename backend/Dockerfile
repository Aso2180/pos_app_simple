# backend/Dockerfile - Azure Container Apps Optimized
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy SSL certificate for Azure MySQL
COPY ./certs/digicert.pem /etc/ssl/certs/digicert.pem
RUN chmod 644 /etc/ssl/certs/digicert.pem

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Health check for Container Apps
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/docs')" || exit 1

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port (Container Apps will override this)
EXPOSE 8000

# Start command - initialize data then run server
CMD ["sh", "-c", "python -m app.init_data || true && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1"]
