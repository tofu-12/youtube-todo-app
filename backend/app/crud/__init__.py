"""CRUD operations."""

from app.crud.recurrence import (
    delete_recurrence,
    get_recurrence_by_video,
    upsert_recurrence,
)
from app.crud.tag import create_tag, delete_tag, get_or_create_tag, get_tags
from app.crud.todo_history import (
    create_todo_history,
    delete_todo_history,
    get_todo_histories,
)
from app.crud.user import create_user, get_user, update_user
from app.crud.video import (
    create_video,
    delete_video,
    get_video,
    get_videos,
    update_video,
)
from app.crud.video_tag import get_video_tags, set_video_tags
from app.crud.workout_history import (
    create_workout_history,
    delete_workout_history,
    get_workout_histories,
)

__all__ = [
    "create_tag",
    "create_todo_history",
    "create_user",
    "create_video",
    "create_workout_history",
    "delete_recurrence",
    "delete_tag",
    "delete_todo_history",
    "delete_video",
    "delete_workout_history",
    "get_or_create_tag",
    "get_recurrence_by_video",
    "get_tags",
    "get_todo_histories",
    "get_user",
    "get_video",
    "get_video_tags",
    "get_videos",
    "get_workout_histories",
    "set_video_tags",
    "update_user",
    "update_video",
    "upsert_recurrence",
]
