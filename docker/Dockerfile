# ======= Stage 1: Build =======
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies for packages like lxml, psycopg2, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libffi-dev \
    libjpeg-dev \
    libavif-dev \
    pkg-config \
    unzip zip \
    curl \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage caching
COPY src/requirements.txt .

# Install Python packages into /install
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .

# ======= Stage 2: Runtime =======
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local
COPY --from=builder /app /app



EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
