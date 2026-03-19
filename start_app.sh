#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME="youtube-todo"
BASE_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$BASE_DIR"

# --- Docker services (db + backend) ---
echo "Starting db + backend..."
docker compose up --build -d

echo "Waiting for backend to be ready..."
until curl -sf http://localhost:8000/health > /dev/null 2>&1; do
    sleep 1
done

echo "Running database migrations..."
docker compose exec backend uv run alembic upgrade head

# --- Install frontend dependencies ---
echo "Installing frontend dependencies..."
cd "$BASE_DIR/frontend" && npm install
cd "$BASE_DIR"

# --- tmux session ---
tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true

tmux new-session -d -s "$SESSION_NAME" -n backend -c "$BASE_DIR"
tmux send-keys -t "$SESSION_NAME:backend" "docker compose logs -f backend" C-m

tmux new-window -t "$SESSION_NAME" -n frontend -c "$BASE_DIR/frontend"
tmux send-keys -t "$SESSION_NAME:frontend" "npm run dev" C-m

# --- Open browser ---
sleep 3
open "http://localhost:3000"

echo "--------------------------------------------------"
echo "tmux セッション '$SESSION_NAME' で全サービスを起動しました。"
echo ""
echo "Backend : http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "セッションにアタッチするには:"
echo "  tmux attach -t $SESSION_NAME"
echo ""
echo "ウィンドウ:"
echo "  backend : tmux select-window -t $SESSION_NAME:backend"
echo "  frontend: tmux select-window -t $SESSION_NAME:frontend"
echo ""
echo "停止する場合:"
echo "  tmux kill-session -t $SESSION_NAME"
echo "  docker compose down"
echo "--------------------------------------------------"
