# ---- Stage 1: Build frontend ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --frozen-lockfile 2>/dev/null || npm install
COPY frontend/ ./
RUN npm run build


# ---- Stage 2: Backend runtime ----
FROM python:3.12-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libffi-dev default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir PyPDF2 python-docx openpyxl asyncpg pgvector

# Copy backend source
COPY backend/ ./

# Copy frontend build (baked into image, not on a volume)
COPY --from=frontend-builder /app/frontend/dist /app/_static_dist

# Create necessary directories
RUN mkdir -p /app/uploads /app/logs /app/storage

EXPOSE 8000

# Start: sync frontend to shared volume, then run API
CMD ["sh", "-c", "cp -r /app/_static_dist/* /app/static/ 2>/dev/null || true; uvicorn app.main:app --host 0.0.0.0 --port 8000"]
