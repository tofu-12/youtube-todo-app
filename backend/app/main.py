"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.recurrences import router as recurrences_router
from app.api.settings import router as settings_router
from app.api.tags import router as tags_router
from app.api.today import router as today_router
from app.api.todo_histories import router as todo_histories_router
from app.api.videos import router as videos_router
from app.api.workout_histories import router as workout_histories_router

app = FastAPI(title="YouTube Todo App")

app.include_router(auth_router)
app.include_router(videos_router)
app.include_router(recurrences_router)
app.include_router(today_router)
app.include_router(settings_router)
app.include_router(tags_router)
app.include_router(todo_histories_router)
app.include_router(workout_histories_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "ok"}
