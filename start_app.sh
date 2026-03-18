#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "==> Starting services (db + backend)..."
docker compose up --build -d

echo "==> Waiting for backend to be ready..."
until curl -sf http://localhost:8000/health > /dev/null 2>&1; do
    sleep 1
done

echo "==> Creating test database (if not exists)..."
docker compose exec db psql -U user -d youtube_todo -c "CREATE DATABASE youtube_todo_test;" 2>/dev/null || true

echo "==> Running database migrations..."
docker compose exec backend uv run alembic upgrade head

echo ""
echo "Backend is running at http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo ""
echo "To stop: docker compose down"
echo "To stop and remove data: docker compose down -v"
