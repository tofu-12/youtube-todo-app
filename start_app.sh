#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

FRONTEND_PID=""

cleanup() {
    echo ""
    echo "==> Stopping frontend dev server..."
    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        kill "$FRONTEND_PID"
        wait "$FRONTEND_PID" 2>/dev/null
    fi
    echo "==> Stopping backend services..."
    docker compose down
    echo "==> All services stopped."
}

trap cleanup EXIT INT TERM

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

echo "==> Installing frontend dependencies..."
cd frontend
npm install

echo "==> Starting frontend dev server..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Backend is running at http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo "Frontend is running at http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services."

wait $FRONTEND_PID
