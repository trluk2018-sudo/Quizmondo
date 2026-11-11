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

# Create unprivileged system user (UID/GID 1000)
RUN groupadd -r -g 1000 appuser && \
    useradd -r -u 1000 -g appuser -d /app -s /sbin/nologin appuser

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

RUN mkdir -p /app/instance /app/uploads /app/data && \
    chmod +x /app/docker-entrypoint.sh 2>/dev/null || true && \
    chown -R appuser:appuser /app

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
# Access logging to stdout, so `docker logs` has a record of every request and
# how long it took. Without it the container logged only its boot lines, and a
# slow or hanging request left no trace anywhere to diagnose from.
#
# %(D)s is the time taken in microseconds -- the field worth having, since it
# is what makes a slow request findable:
#   docker logs <container> | awk '$NF+0 > 1000000'   # slower than a second
#
# --timeout is set to gunicorn's own default rather than changed, so it is
# visible and deliberate instead of implied.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", \
     "--workers", "2", "--threads", "4", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--access-logformat", "%(h)s \"%(r)s\" %(s)s %(b)sb %(D)sus", \
     "run:app"]
