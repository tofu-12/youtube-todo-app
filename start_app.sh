#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

cleanup() {
    echo ""
    echo "Stopping all services..."
    docker compose down
    echo "All services stopped."
}

trap cleanup EXIT INT TERM

echo "Starting all services..."
docker compose up --build -d

echo "Waiting for backend to be ready..."
until curl -sf http://localhost:8000/health > /dev/null 2>&1; do
    sleep 1
done

echo "Running database migrations..."
docker compose exec backend uv run alembic upgrade head

echo ""
echo "Backend is running at http://localhost:8000"
echo "Frontend is running at http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services."

# Block until Ctrl+C
sleep infinity
