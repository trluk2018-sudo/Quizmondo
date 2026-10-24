# --- Stage 1: Build CSS with Tailwind ---
FROM node:20-alpine AS css-builder
WORKDIR /build
COPY package*.json ./
RUN npm ci
COPY src/ ./src/
COPY app/ ./app/
RUN npm run build:css

# --- Stage 2: Python Application Runner ---
FROM python:3.11-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .
# Copy compiled CSS from Stage 1
COPY --from=css-builder /build/app/static/css/tailwind.min.css ./app/static/css/tailwind.min.css

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "run:app"]
