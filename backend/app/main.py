"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="YouTube Todo App")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "ok"}
